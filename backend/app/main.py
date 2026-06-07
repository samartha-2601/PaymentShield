from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router

from app.models.base import Base
from app.core.database import engine

from app.api.config_test import router as config_router
from app.api.payments import router as payment_router
from app.api.webhooks import router as webhook_router
from app.api.payments_data import router as payments_data_router
from app.api.alerts import router as alerts_router
from app.api.dashboard import router as dashboard_router

import app.models.payment
import app.models.alert

app = FastAPI(
    title="PaymentShield API",
    description="Security-focused payment intelligence platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
Base.metadata.create_all(bind=engine)
app.include_router(config_router)
app.include_router(payment_router)
app.include_router(webhook_router)
app.include_router(payments_data_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "application": "PaymentShield",
        "status": "running",
        "version": "1.0.0"
    }