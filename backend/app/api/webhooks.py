import stripe

from fastapi import APIRouter
from fastapi import Request
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal

from app.models.payment import Payment
from app.models.alert import Alert
from app.models.processed_event import ProcessedEvent

from app.services.audit_service import (
    create_audit_log
)

from app.services.risk_engine import (
    calculate_risk_score,
    determine_alert_type
)

from app.services.card_testing import (
    detect_card_testing
)

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"]
)


@router.post("/stripe")
async def stripe_webhook(request: Request):

    payload = await request.body()

    sig_header = request.headers.get(
        "stripe-signature"
    )

    try:

        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe signature"
        )

    event_type = event["type"]
    event_id = event["id"]

    db: Session = SessionLocal()

    try:

        # =====================================
        # Replay Attack Protection
        # =====================================

        existing_event = (
            db.query(ProcessedEvent)
            .filter(
                ProcessedEvent.stripe_event_id == event_id
            )
            .first()
        )

        if existing_event:

            create_audit_log(
                db,
                event_id,
                event_type,
                "DUPLICATE",
                "Replay attack prevented"
            )

            return {
                "received": True,
                "duplicate": True
            }

        processed_event = ProcessedEvent(
            stripe_event_id=event_id
        )

        db.add(processed_event)
        db.commit()

        create_audit_log(
            db,
            event_id,
            event_type,
            "ACCEPTED",
            "Stripe event processed"
        )

        # =====================================
        # Process Checkout Event
        # =====================================

        if event_type == "checkout.session.completed":

            data = event["data"]["object"]

            amount = data["amount_total"] / 100

            risk_score = calculate_risk_score(
                amount
            )

            customer_email = None

            try:
                customer_email = (
                    data["customer_details"]["email"]
                )
            except Exception:
                pass

            payment = Payment(
                stripe_payment_id=data["payment_intent"],
                customer_email=customer_email,
                amount=amount,
                status="succeeded",
                risk_score=risk_score
            )

            db.add(payment)
            db.commit()
            db.refresh(payment)

            # =====================================
            # Card Testing Detection
            # =====================================

            if customer_email:

                card_testing_detected = (
                    detect_card_testing(
                        db,
                        customer_email
                    )
                )

                if card_testing_detected:

                    existing_card_testing_alert = (
                        db.query(Alert)
                        .filter(
                            Alert.alert_type ==
                            "Card Testing"
                        )
                        .filter(
                            Alert.status == "OPEN"
                        )
                        .first()
                    )

                    if not existing_card_testing_alert:

                        card_testing_alert = Alert(
                            payment_id=payment.id,
                            alert_type="Card Testing",
                            severity="HIGH",
                            description=(
                                "Multiple low-value "
                                "transactions detected "
                                "within 10 minutes"
                            ),
                            status="OPEN"
                        )

                        db.add(card_testing_alert)
                        db.commit()

            # =====================================
            # Transaction Risk Alerts
            # =====================================

            alert = determine_alert_type(
                risk_score
            )

            if alert:

                alert_type, severity, description = alert

                new_alert = Alert(
                    payment_id=payment.id,
                    alert_type=alert_type,
                    severity=severity,
                    description=description,
                    status="OPEN"
                )

                db.add(new_alert)
                db.commit()

    finally:

        db.close()

    return {
        "received": True
    }