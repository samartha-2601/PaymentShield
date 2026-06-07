from fastapi import APIRouter

from app.core.database import SessionLocal
from app.models.alert import Alert

router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get("/alerts")
def get_alerts():

    db = SessionLocal()

    alerts = db.query(Alert).all()

    result = []

    for alert in alerts:
        result.append({
            "id": alert.id,
            "type": alert.alert_type,
            "severity": alert.severity,
            "description": alert.description
        })

    db.close()

    return result