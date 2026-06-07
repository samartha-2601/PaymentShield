from fastapi import APIRouter

from app.core.database import SessionLocal
from app.models.payment import Payment

router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get("/payments")
def get_payments():

    db = SessionLocal()

    payments = db.query(Payment).all()

    result = []

    for payment in payments:
        result.append({
            "id": payment.id,
            "email": payment.customer_email,
            "amount": payment.amount,
            "status": payment.status,
            "risk_score": payment.risk_score
        })

    db.close()

    return result