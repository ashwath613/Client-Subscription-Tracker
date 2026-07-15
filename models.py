from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey,
    Enum
)

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime

import enum



# restricting the values using enum
class PlanType(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    PAST_DUE = "past_due"


# creation of customer table

class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship(
        "Subscription",
        back_populates="customer"
    )



# creation of subscription table 

class Subscription(Base):

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    plan_type = Column(
        Enum(PlanType),
        nullable=False
    )

    status = Column(
        Enum(SubscriptionStatus),
        nullable=False
    )

    usage_limit = Column(
        Integer,
        nullable=False
    )

    current_usage = Column(
        Integer,
        default=0
    )

    billing_start = Column(Date)

    billing_end = Column(Date)

    customer = relationship(
        "Customer",
        back_populates="subscriptions"
    )