# Auth By Pageless

Production-ready Authentication & Identity Module built with FastAPI, PostgreSQL, SQLAlchemy, Redis, JWT, OAuth, and Alembic.

Version: v1.0.0

---

## Overview

Auth By Pageless is a reusable authentication backend designed for all Pageless products and future SaaS applications.

The system provides:

* User Authentication
* User Management
* Session Management
* JWT Access Tokens
* JWT Refresh Tokens
* Google OAuth
* GitHub OAuth
* Multi-Device Sessions
* Redis Integration
* Account Verification
* OAuth Account Linking
* OAuth Account Unlinking
* Password Setup for OAuth Users

The architecture is modular and can be integrated into any FastAPI-based application.

---

## Features

### Authentication

* User Registration
* User Login
* User Logout
* Current User Endpoint
* Access Token Generation
* Refresh Token Generation
* Token Refresh
* Password Hashing
* Password Validation

### User Management

* User Profiles
* Profile Updates
* User Search
* User Verification
* User Activation
* User Deactivation
* User Statistics

### Session Management

* Device Sessions
* Session Tracking
* Logout Single Device
* Logout All Devices
* Session Analytics
* Suspicious Session Detection
* Refresh Token Storage

### OAuth

#### Google OAuth

* Login with Google
* Automatic Account Creation
* Existing Account Linking
* Account Unlinking

#### GitHub OAuth

* Login with GitHub
* Automatic Account Creation
* Existing Account Linking
* Account Unlinking

### Security

* JWT Authentication
* Refresh Token Rotation
* Password Hashing
* OAuth + Password Hybrid Accounts
* Account Verification
* Last Login Tracking

### Infrastructure

* FastAPI
* Async SQLAlchemy
* PostgreSQL
* Redis
* Alembic Migrations
* Docker Ready
* Kubernetes Ready

---

## Technology Stack

| Layer          | Technology       |
| -------------- | ---------------- |
| API            | FastAPI          |
| Database       | PostgreSQL       |
| ORM            | SQLAlchemy Async |
| Migrations     | Alembic          |
| Cache          | Redis            |
| Authentication | JWT              |
| OAuth          | Authlib          |
| Validation     | Pydantic v2      |
| Deployment     | Docker           |
| Orchestration  | Kubernetes       |

---

## Project Structure

```text
authentification/
│
├── backend/
│   │
│   ├── app/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── sessions/
│   │   ├── oauth/
│   │   ├── core/
│   │   └── common/
│   │
│   ├── alembic/
│   ├── docker/
│   ├── k8s/
│   │
│   ├── db.py
│   ├── main.py
│   ├── requirements.txt
│   └── docker-compose.yml
│
├── README.md
└── .gitignore
```

---

## Installation

Clone Repository

```bash
git clone https://github.com/Lithin-kumar-v/auth-by-pageless.git
```

```bash
cd auth-by-pageless/backend
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a .env file.

```env
APP_NAME=Pageless Gradient
APP_ENV=development

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/pageless

REDIS_URL=redis://localhost:6379

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

ACCESS_TOKEN_MINUTES=30
REFRESH_TOKEN_DAYS=7

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

---

## Database Migration

Create Tables

```bash
alembic upgrade head
```

Create Migration

```bash
alembic revision --autogenerate -m "message"
```

Apply Migration

```bash
alembic upgrade head
```

---

## Run Application

```bash
uvicorn main:app --reload
```

Swagger

```text
http://127.0.0.1:8000/docs
```

OpenAPI

```text
http://127.0.0.1:8000/openapi.json
```

---

## Available Modules

### Auth Module

Responsible for:

* Registration
* Login
* Refresh
* Logout
* Current User

### Users Module

Responsible for:

* User Management
* Profiles
* Verification
* Search

### Sessions Module

Responsible for:

* Device Tracking
* Session Analytics
* Session Security

### OAuth Module

Responsible for:

* Google OAuth
* GitHub OAuth
* Account Linking
* Account Unlinking

---

## API Endpoints

### Authentication

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
```

### Users

```text
GET    /api/v1/users/me
PATCH  /api/v1/users/me
GET    /api/v1/users/me/profile
PATCH  /api/v1/users/me/profile
```

### Sessions

```text
GET    /api/v1/sessions
GET    /api/v1/sessions/current
POST   /api/v1/sessions/logout-all
DELETE /api/v1/sessions/{session_id}
```

### OAuth

```text
GET    /api/v1/oauth/google/login
GET    /api/v1/oauth/google/callback

GET    /api/v1/oauth/github/login
GET    /api/v1/oauth/github/callback

POST   /api/v1/oauth/set-password

GET    /api/v1/oauth/providers
GET    /api/v1/oauth/linked-providers

DELETE /api/v1/oauth/google/unlink
DELETE /api/v1/oauth/github/unlink
```

---

## Current Version

### v1.0.0

Implemented

* Authentication System
* User Management
* Session Management
* Google OAuth
* GitHub OAuth
* Redis Integration
* Alembic Migrations
* Docker Support
* Kubernetes Readiness

---

## Roadmap

### v1.1.0

* Email Verification
* Forgot Password
* Password Reset
* Rate Limiting

### v1.2.0

* Multi-Factor Authentication
* TOTP
* Recovery Codes

### v2.0.0

* RBAC
* Organizations
* API Keys
* SSO

---

## License

Private Repository

Copyright © 2026 Pageless.

All rights reserved.

---

## Author

Lithin Kumar V

GitHub:
https://github.com/Lithin-kumar-v

Project:
Auth By Pageless
