from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    stripe_payment_id = Column(String, unique=True)

    customer_email = Column(String)

    amount = Column(Float)

    status = Column(String)

    risk_score = Column(Integer, default=0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )