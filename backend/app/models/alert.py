from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    payment_id = Column(Integer)

    alert_type = Column(String)

    severity = Column(String)

    description = Column(String)