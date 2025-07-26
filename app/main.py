
from fastapi import FastAPI
from app.api.routers import product,customer,category,invoice,auth,dashboard,user
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Construction Hardware Shop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://globalbuildhub.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(invoice.router, prefix="/invoices", tags=["Invoices"])
# app.include_router(report.router, prefix="/reports", tags=["Reports"])
app.include_router(customer.router, prefix="/customers", tags=["Customers"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(auth.router)
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(user.router, prefix="/users", tags=["Users"])
