from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles

from database import Base, engine, get_db
import models
import schemas
import crud

from datetime import date

app = FastAPI(
    title="Client Subscription Tracker"
)
# used for fetch css styles from css file in static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# html template
templates = Jinja2Templates(directory="templates")

# Create Tables
Base.metadata.create_all(bind=engine)


#dashboard home
@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    customers = crud.get_dashboard_data(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "customers": customers
        }
    )


#end point  with create function to creat the customers

@app.post(
    "/customers",
    response_model=schemas.CustomerResponse
)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):

    return crud.create_customer(db, customer)


#endpoint with create function to add subscription to the customer

@app.post(
    "/subscriptions",
    response_model=schemas.SubscriptionResponse
)
def create_subscription(
    subscription: schemas.SubscriptionCreate,
    db: Session = Depends(get_db)
):

    customer = crud.get_customer(
        db,
        subscription.customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return crud.create_subscription(
        db,
        subscription
    )


# end point with customer usage updation function

@app.post("/subscriptions/{subscription_id}/usage")
def record_usage(
    subscription_id: int,
    usage: schemas.UsageRequest,
    db: Session = Depends(get_db)
):

    try:

        subscription = crud.record_usage(
            db,
            subscription_id,
            usage.usage
        )

        if subscription is None:

            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        return {

            "message": "Usage Updated Successfully",
            "current_usage": subscription.current_usage,
            "usage_limit": subscription.usage_limit

        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


#end point with user usage calculation in percentage

@app.get("/subscriptions/{subscription_id}")
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    subscription = crud.get_subscription(
        db,
        subscription_id
    )

    if subscription is None:

        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    usage_percent = round(

        (
            subscription.current_usage /
            subscription.usage_limit
        ) * 100,

        2

    )

    days_remaining = (

        subscription.billing_end -
        date.today()

    ).days

    return {

        "id": subscription.id,
        "plan_type": subscription.plan_type,
        "status": subscription.status,
        "usage_limit": subscription.usage_limit,
        "current_usage": subscription.current_usage,
        "usage_percent": usage_percent,
        "days_remaining": days_remaining

    }



# customer plus subscription

@app.get("/customer/{customer_id}", response_class=HTMLResponse)
def customer_page(
    customer_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    customer = crud.get_customer(db, customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    subscriptions = crud.get_customer_subscriptions(
        db,
        customer_id
    )

    return templates.TemplateResponse(

        "customer.html",

        {
            "request": request,
            "customer": customer,
            "subscriptions": subscriptions
        }

    )