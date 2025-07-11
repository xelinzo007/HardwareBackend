from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models.invoice import Invoice

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    compare: bool = Query(True)
):
    # Current period
    invoices = db.query(Invoice).filter(Invoice.date.between(start_date, end_date)).all()
    total_sales = sum(inv.final_total_after_discount for inv in invoices)
    total_credit = sum(inv.final_total_after_discount for inv in invoices if inv.payment_mode.lower() == "credit")
    total_invoices = len(invoices)

    result = {
        "total_sales": total_sales,
        "total_credit": total_credit,
        "total_invoices": total_invoices,
        "start_date": start_date,
        "end_date": end_date,
    }

    # Previous period for comparison
    if compare:
        delta = end_date - start_date
        prev_start = start_date - delta
        prev_end = end_date - delta

        prev_invoices = db.query(Invoice).filter(Invoice.date.between(prev_start, prev_end)).all()
        prev_sales = sum(inv.final_total_after_discount for inv in prev_invoices)
        prev_credit = sum(inv.final_total_after_discount for inv in prev_invoices if inv.payment_mode.lower() == "credit")
        prev_count = len(prev_invoices)

        def calc_percent_change(current, previous):
            if previous == 0:
                return 100.0 if current > 0 else 0.0
            return ((current - previous) / previous) * 100

        result.update({
            "sales_change_pct": calc_percent_change(total_sales, prev_sales),
            "credit_change_pct": calc_percent_change(total_credit, prev_credit),
            "invoice_change_pct": calc_percent_change(total_invoices, prev_count)
        })

    return result
