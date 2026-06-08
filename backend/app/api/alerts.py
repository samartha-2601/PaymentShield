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
            "description": alert.description,
            "status": alert.status
        })

    db.close()

    return result


@router.put("/alerts/{alert_id}/investigate")
def investigate_alert(alert_id: int):

    db = SessionLocal()

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:

        db.close()

        return {
            "error": "Alert not found"
        }

    alert.status = "INVESTIGATING"

    db.commit()

    db.close()

    return {
        "message": "Alert updated",
        "status": "INVESTIGATING"
    }


@router.put("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int):

    db = SessionLocal()

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:

        db.close()

        return {
            "error": "Alert not found"
        }

    alert.status = "RESOLVED"

    db.commit()

    db.close()

    return {
        "message": "Alert resolved",
        "status": "RESOLVED"
    }