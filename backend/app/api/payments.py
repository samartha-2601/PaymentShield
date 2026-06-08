from fastapi import APIRouter
import stripe

from app.core.config import settings

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/checkout")
def create_checkout_session():

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "PaymentShield Demo Product"
                    },
                    "unit_amount": 100,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:5173/success",
        cancel_url="http://localhost:5173"
    )

    return {
        "checkout_url": session.url,
        "session_id": session.id
    }