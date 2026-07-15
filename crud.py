from sqlalchemy.orm import Session
from models import Customer, Subscription
from schemas import CustomerCreate, SubscriptionCreate
from datetime import date


# creat function to add customer data into database
def create_customer(db: Session, customer: CustomerCreate):

    new_customer = Customer(
        name=customer.name,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


#create or add the subscription details in database (one to many realtionalship) one customer have multiple subscriptions 
def create_subscription(db: Session, subscription: SubscriptionCreate):

    new_subscription = Subscription(

        customer_id=subscription.customer_id,

        plan_type=subscription.plan_type,

        status=subscription.status,

        usage_limit=subscription.usage_limit,

        current_usage=0,

        billing_start=subscription.billing_start,

        billing_end=subscription.billing_end

    )

    db.add(new_subscription)

    db.commit()

    db.refresh(new_subscription)

    return new_subscription



#return customer details using customer Id

def get_customer(db: Session, customer_id: int):

    return db.query(Customer).filter(
        Customer.id == customer_id
    ).first()


# --------------------------------------------------
# GET SUBSCRIPTION


def get_subscription(db: Session, subscription_id: int):

    return db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()


# --------------------------------------------------
# GET ALL SUBSCRIPTIONS
# --------------------------------------------------

def get_customer_subscriptions(
        db: Session,
        customer_id: int
):

    return db.query(Subscription).filter(
        Subscription.customer_id == customer_id
    ).all()


# --------------------------------------------------
# RECORD USAGE
# --------------------------------------------------

def record_usage(
        db: Session,
        subscription_id: int,
        usage: int
):

    subscription = get_subscription(
        db,
        subscription_id
    )

    if subscription is None:

        return None

    new_usage = subscription.current_usage + usage

    if new_usage > subscription.usage_limit:

        raise ValueError(
            "Usage limit exceeded"
        )

    subscription.current_usage = new_usage

    db.commit()

    db.refresh(subscription)

    return subscription


#fetch details of customer info and subscription info into dashboard

def get_dashboard_data(db: Session):

    customers = db.query(Customer).all()

    dashboard = []

    for customer in customers:

        if customer.subscriptions:

            latest = customer.subscriptions[-1]

            usage_percent = round(
                (latest.current_usage / latest.usage_limit) * 100,
                2
            )

            dashboard.append({

                "customer_id": customer.id,

                "customer_name": customer.name,

                "email": customer.email,

                "plan": latest.plan_type.value,

                "status": latest.status.value,

                "current_usage": latest.current_usage,

                "usage_limit": latest.usage_limit,

                "usage_percent": usage_percent

            })

        else:

            dashboard.append({

                "customer_id": customer.id,

                "customer_name": customer.name,

                "email": customer.email,

                "plan": "-",

                "status": "-",

                "current_usage": 0,

                "usage_limit": 0,

                "usage_percent": 0

            })

    return dashboard