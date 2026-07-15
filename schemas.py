from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from enum import Enum


#attribute enum
class PlanType(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    PAST_DUE = "past_due"


# customer table as python class

class CustomerCreate(BaseModel):

    name: str

    email: EmailStr

# customer response model for visulaization
class CustomerResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    created_at: datetime

    class Config:
        from_attributes = True


# subscription table in python class

class SubscriptionCreate(BaseModel):

    customer_id: int

    plan_type: PlanType

    status: SubscriptionStatus

    usage_limit: int

    billing_start: date

    billing_end: date

#subscriptions response model
class SubscriptionResponse(BaseModel):

    id: int

    customer_id: int

    plan_type: PlanType

    status: SubscriptionStatus

    usage_limit: int

    current_usage: int

    billing_start: date

    billing_end: date

    class Config:
        from_attributes = True


# record usuage

class UsageRequest(BaseModel):

    usage: int