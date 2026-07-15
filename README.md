# Client Subscription Tracker

A lightweight subscription management application built using **FastAPI**, **SQLAlchemy**, **PostgreSQL (Neon Cloud)**, and **Jinja2**.

The project was developed as part of a backend technical assessment to demonstrate API development, database design, business rule implementation, server-side rendering, and PostgreSQL integration.

---

# Features

* Create customers
* Create subscriptions for customers
* Track subscription usage
* Prevent usage from exceeding the configured plan limit
* View subscription details
* View customer subscription history
* Dashboard showing customer plans and usage
* REST APIs with automatic validation using FastAPI and Pydantic
* Server-rendered dashboard using Jinja2

---

# Tech Stack

* Python 3.x
* FastAPI
* SQLAlchemy ORM
* PostgreSQL (Neon Cloud)
* Pydantic
* Jinja2
* HTML
* CSS
* Uvicorn

---

# Why I Used Neon Cloud PostgreSQL Instead of a Local Database

I chose **Neon Cloud PostgreSQL** because it provides a fully managed PostgreSQL environment without requiring a local installation.

Some advantages are:

* No local PostgreSQL installation required
* Easy database sharing during development
* Secure cloud-hosted PostgreSQL
* Reliable backups and managed infrastructure
* Same PostgreSQL features available in production
* Easy connection using a single connection string

Neon Website:

https://neon.tech/

---

# Project Structure

```text
ClientSubscriptionTracker/
│
├── main.py
├── crud.py
├── models.py
├── schemas.py
├── database.py
│
├── templates/
│   ├── dashboard.html
│   └── customer.html
│
├── static/
│   └── style.css
│
├── .env
├── requirements.txt
└── README.md
```

---

## Database Configuration

This project uses **Neon Cloud PostgreSQL** instead of a locally installed PostgreSQL database.

The project has already been configured with a `.env` file containing the required `DATABASE_URL`, so no additional database configuration is needed to run the application.

If you would like to view the database directly, you can log in to the Neon dashboard using the credentials
1. User mail id: nashwath613@gmail.com
2. Password: Ashwath@12

**Neon Website:** https://neon.tech

After logging in, you will be able to:

* View the project database
* Browse the `customers` and `subscriptions` tables
* Verify the sample data used in this project
* Execute SQL queries directly from the Neon SQL Editor (if needed)

> 

# Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

---

### 2. Move into the project directory

```bash
cd ClientSubscriptionTracker
```

---

### 3. Create a virtual environment

Windows

```bash
python -m venv venv
```

---

### 4. Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---


### 7. Run the application

```bash
uvicorn main:app --reload
```

---

# Application URLs

Dashboard

```
http://127.0.0.1:8000/
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

Dashboard JSON API

```
http://127.0.0.1:8000/dashboard
```

---

# API Endpoints

| Method | Endpoint                                 | Description               |
| ------ | ---------------------------------------- | ------------------------- |
| POST   | `/customers`                             | Create a customer         |
| POST   | `/subscriptions`                         | Create a subscription     |
| POST   | `/subscriptions/{subscription_id}/usage` | Record subscription usage |
| GET    | `/subscriptions/{subscription_id}`       | Get subscription details  |
| GET    | `/`                                      | Dashboard UI              |
| GET    | `/customer/{customer_id}`                | Customer details page     |

---

# Project Workflow

```text
Client Request
      │
      ▼
FastAPI Routes (main.py)
      │
      ▼
Business Logic (crud.py)
      │
      ▼
SQLAlchemy ORM
      │
      ▼
Neon PostgreSQL Database
      │
      ▼
Response
      │
      ▼
JSON API / Jinja2 Dashboard
```

---

# Database Design

Customer

* id
* name
* email
* created_at

Subscription

* id
* customer_id
* plan_type
* status
* usage_limit
* current_usage
* billing_start
* billing_end

Relationship

One Customer → Many Subscriptions

---

# Business Rules Implemented

* Customer email must be unique.
* Subscription must belong to an existing customer.
* Usage cannot exceed the configured plan limit.
* Invalid requests return appropriate HTTP error responses.
* Request and response validation is handled using Pydantic.

---

# Demo Flow

1. Create a customer.
2. Create a subscription.
3. Record subscription usage.
4. View dashboard.
5. Open customer details.
6. View subscription information.

---

# Notes

This project focuses on backend development using FastAPI and PostgreSQL.

For the frontend, I referred to AI-assisted suggestions for parts of the HTML/CSS layout while implementing and integrating the pages into the FastAPI application myself. The backend architecture, API implementation, database integration, business logic, and overall project structure were designed and implemented as part of this assignment.

---

# Repository

This repository is intended to demonstrate:

* FastAPI REST API development
* SQLAlchemy ORM
* PostgreSQL integration
* Server-side rendering using Jinja2
* Pydantic validation
* Clean project structure
* Business rule implementation
