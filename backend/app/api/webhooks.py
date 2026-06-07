from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.payment import Payment
from app.models.alert import Alert

from app.services.risk_engine import (
    calculate_risk_score,
    determine_alert_type
)

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

        try:

            amount = data.get("amount_total", 0) / 100

            risk_score = calculate_risk_score(amount)

            payment = Payment(
                stripe_payment_id=data.get("payment_intent"),
                customer_email=data.get(
                    "customer_details", {}
                ).get("email"),
                amount=amount,
                status="succeeded",
                risk_score=risk_score
            )

            db.add(payment)
            db.commit()
            db.refresh(payment)

            alert = determine_alert_type(risk_score)

            if alert:

                alert_type, severity, description = alert

                new_alert = Alert(
                    payment_id=payment.id,
                    alert_type=alert_type,
                    severity=severity,
                    description=description
                )

                db.add(new_alert)
                db.commit()

        finally:

            db.close()

    return {
        "received": True
    }