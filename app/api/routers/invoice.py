from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.database import get_db
from app.db.models.customer import Customer
from app.db.models.product import Product
from app.db.models.invoice import Invoice
from app.db.models.invoice_item import InvoiceItem
from app.schemas.invoice import InvoiceIn, InvoiceOut, ProductItem, CustomerIn

router = APIRouter()

@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice_data: InvoiceIn, db: Session = Depends(get_db)):
    customer_data = invoice_data.customer
    customer = db.query(Customer).filter(Customer.phone == customer_data.phone).first()
    if not customer:
        customer = Customer(
            customer_name=customer_data.customer_name,
            phone=customer_data.phone,
            address=customer_data.address
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    items = []
    total_before_tax = 0
    total_gst = 0

    for item in invoice_data.items:
        db_product = db.query(Product).filter(Product.product_code == item.product_code).first()
        if not db_product:
            raise HTTPException(status_code=404, detail=f"Product '{item.product_code}' not found")
        if db_product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {db_product.product_name}")

        db_product.quantity -= item.quantity

        line_total = item.price_per_unit * item.quantity - item.discount
        gst_amount = (line_total * item.gst_percent) / 100
        total_before_tax += line_total
        total_gst += gst_amount

        invoice_item = InvoiceItem(
            product_id=db_product.id,
            product_code=item.product_code,
            product_name=item.product_name,
            category=item.category,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit,
            discount=item.discount,
            gst_percent=item.gst_percent
        )
        items.append(invoice_item)

    taxable_amount = total_before_tax + total_gst
    invoice_discount = (invoice_data.discount_percentage / 100) * taxable_amount
    final_total = taxable_amount - invoice_discount

    invoice = Invoice(
        invoice_id=f"INV-{uuid4().hex[:8].upper()}",
        customer_id=customer.id,
        customer_name=customer.customer_name,
        phone=customer.phone,
        address=customer.address,
        payment_mode=invoice_data.payment_mode,
        total_before_tax=total_before_tax,
        gst_amount=total_gst,
        taxable_amount=taxable_amount,
        discount=invoice_discount,
        final_total_after_discount=final_total,
        items=items
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return InvoiceOut(
        invoice_id=invoice.invoice_id,
        date=invoice.date,
        time=invoice.time,
        customer=CustomerIn(
            customer_name=customer.customer_name,
            address=customer.address,
            phone=customer.phone
        ),
        items=[ProductItem(**item.__dict__) for item in items],
        total_before_tax=total_before_tax,
        gst_amount=total_gst,
        taxable_amount=taxable_amount,
        total_amount=taxable_amount,
        discount=invoice_discount,
        final_total_after_discount=final_total,
        payment_mode=invoice.payment_mode
    )

@router.get("/")
def get_all_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    results = []
    for invoice in invoices:
        results.append({
            "invoice_id": invoice.invoice_id,
            "date": invoice.date,
            "time": invoice.time,
            "customer_name": invoice.customer_name,
            "phone": invoice.phone,
            "payment_mode": invoice.payment_mode,
            "total": invoice.final_total_after_discount,
            "items": [
                {
                    "product_code": item.product_code,
                    "product_name": item.product_name,
                    "category": item.category,
                    "quantity": item.quantity,
                    "price_per_unit": item.price_per_unit,
                    "gst_percent": item.gst_percent,
                    "discount": item.discount
                } for item in invoice.items
            ]
        })
    return results

@router.get("/by-phone/{phone}")
def get_invoices_by_phone(phone: str, db: Session = Depends(get_db)):
    return db.query(Invoice).filter(Invoice.phone == phone).all()

@router.get("/by-id/{invoice_id}")
def get_invoice_by_id(invoice_id: str, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        "invoice_id": invoice.invoice_id,
        "date": invoice.date,
        "time": invoice.time,
        "customer_name": invoice.customer_name,
        "phone": invoice.phone,
        "payment_mode": invoice.payment_mode,
        "total": invoice.final_total_after_discount,
        "items": [
            {
                "product_code": item.product_code,
                "product_name": item.product_name,
                "category": item.category,
                "quantity": item.quantity,
                "price_per_unit": item.price_per_unit,
                "gst_percent": item.gst_percent,
                "discount": item.discount
            } for item in invoice.items
        ]
    }

@router.delete("/{invoice_id}", status_code=200)
def delete_invoice(invoice_id: str, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Restore product stock
    for item in invoice.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.quantity += item.quantity

    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted successfully"}
