from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    event_id = Column(String)

    event_type = Column(String)

    action = Column(String)

    message = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )