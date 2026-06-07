from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/config-test")
def config_test():

    return {
        "stripe_secret_loaded": bool(settings.STRIPE_SECRET_KEY),
        "stripe_publishable_loaded": bool(settings.STRIPE_PUBLISHABLE_KEY)
    }