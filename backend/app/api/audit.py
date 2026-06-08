from fastapi import APIRouter

from app.core.database import SessionLocal
from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/audit",
    tags=["audit"]
)


@router.get("/logs")
def get_audit_logs():

    db = SessionLocal()

    logs = (
        db.query(AuditLog)
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )

    result = []

    for log in logs:

        result.append({
            "event_id": log.event_id,
            "event_type": log.event_type,
            "action": log.action,
            "message": log.message,
            "created_at": str(log.created_at)
        })

    db.close()

    return result