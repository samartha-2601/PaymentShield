from fastapi import APIRouter
from fastapi import Request
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.payment import Payment

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"]
)


@router.post("/stripe")
async def stripe_webhook(request: Request):

    payload = await request.json()

    event_type = payload.get("type")

    if event_type == "checkout.session.completed":

        data = payload["data"]["object"]

        db: Session = SessionLocal()

        payment = Payment(
            stripe_payment_id=data.get("payment_intent"),
            customer_email=data.get("customer_details", {}).get("email"),
            amount=(data.get("amount_total", 0) / 100),
            status="succeeded",
            risk_score=0
        )

        db.add(payment)
        db.commit()

        db.close()

    return {
        "received": True
    }