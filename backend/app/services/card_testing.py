from datetime import datetime
from datetime import timedelta

from app.models.payment import Payment


def detect_card_testing(
    db,
    customer_email
):

    ten_minutes_ago = (
        datetime.utcnow()
        - timedelta(minutes=10)
    )

    recent_payments = (
        db.query(Payment)
        .filter(
            Payment.customer_email == customer_email
        )
        .filter(
            Payment.amount <= 10
        )
        .filter(
            Payment.created_at >= ten_minutes_ago
        )
        .count()
    )

    return recent_payments >= 3