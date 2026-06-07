from fastapi import APIRouter
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.payment import Payment
from app.models.alert import Alert

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get("/summary")
def dashboard_summary():

    db = SessionLocal()

    total_payments = db.query(Payment).count()

    total_alerts = db.query(Alert).count()

    revenue = (
        db.query(func.sum(Payment.amount))
        .scalar()
    ) or 0

    db.close()

    return {
        "payments": total_payments,
        "alerts": total_alerts,
        "revenue": revenue
    }