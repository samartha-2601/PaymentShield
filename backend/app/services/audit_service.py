from app.models.audit_log import AuditLog


def create_audit_log(
    db,
    event_id,
    event_type,
    action,
    message
):

    log = AuditLog(
        event_id=event_id,
        event_type=event_type,
        action=action,
        message=message
    )

    db.add(log)
    db.commit()