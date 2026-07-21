# Intellex AI - Backend Foundation

Welcome to the backend architecture for **Intellex AI** — a premium, enterprise-ready AI Assistant. This directory houses the production-ready Python backend foundation, designed utilizing clean, modular, and enterprise-grade architecture.

---

## 🏗 Architecture Blueprint

The project follows a **modular, clean architecture pattern** centered around FastAPI, SQLAlchemy 2.0, and Pydantic v2:

```
backend/
├── app/
│   ├── api/             # API Router registrations (v1)
│   ├── config/          # Central settings, environment variables parsing (Pydantic Settings v2)
│   ├── constants/       # Global constants, message templates
│   ├── core/            # Core setups (advanced structured JSON logging)
│   ├── database/        # DB engines, session factories, Alembic migration files
│   ├── dependencies/    # FastAPI dependency injections (DB sessions, validators)
│   ├── exceptions/      # Centralized HTTP exception handlers
│   ├── middleware/      # Performance monitoring, Request-ID tracing, CORS
│   ├── models/          # SQLAlchemy DB models mapping
│   ├── routes/          # Health check, feature endpoints
│   ├── schemas/         # Pydantic validation & serialization models
│   ├── services/        # Decoupled business logic services
│   ├── utils/           # Shared helper functions (files, text processors)
│   └── main.py          # Application bootstrapper and lifespan events
├── tests/               # Integrated Pytest suite
├── scripts/             # Execution and utility automation scripts
├── uploads/             # Managed user uploads storage
├── logs/                # Structured application logs storage
├── Dockerfile           # Multi-stage optimized Docker build
├── docker-compose.yml   # Multi-service setup (App + PostgreSQL)
└── requirements.txt     # Locked production dependencies
```

---

## 🛠 Prerequisites

Ensure you have the following installed on your host machine:
* Python 3.12+
* Docker & Docker Compose (optional but recommended)
* PostgreSQL (if running locally without Docker)

---

## 🚀 Quick Start Guide

### 1. Local Environment Setup

Clone the repository and navigate into the backend folder:
```bash
cd backend
```

Create a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install core dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration (`.env`)

Initialize your local configuration by copying `.env.example`:
```bash
cp .env.example .env
```
Update `.env` values (such as database credentials or storage limits) as needed.

### 3. Database Migrations

Apply database schema migrations using Alembic:
```bash
alembic upgrade head
```

### 4. Running the Server

Start the development server with Uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```
Your backend will be live at `http://localhost:8000`. You can inspect the interactive OpenAPI Swagger documentation at:
👉 **`http://localhost:8000/docs`**

---

## 🐳 Docker Deployment

To launch the entire backend stack including a ready-to-use PostgreSQL database:

```bash
docker-compose up --build -d
```

* **Backend Service**: `http://localhost:8000`
* **PostgreSQL Service**: `localhost:5432`

To stop services:
```bash
docker-compose down
```

---

## 🧪 Testing

The pytest framework is configured and ready to run. Executing unit and integration tests is simple:

```bash
pytest
```

---

## 🛡 Features & Architectural Safeguards

1. **Robust Configuration Management**: Backed by Pydantic's `BaseSettings`. Auto-validates system environment variables at boot.
2. **PostgreSQL & SQLAlchemy 2.0**: Integrated modern asynchronous engine management with thread-safe session containment.
3. **Structured JSON Logging**: Centralized logging logic ensuring production logs are fully auditable and structured.
4. **Custom Exception Handler**: Standardized unified error API responses mapping DB failures, validation issues, or server crashes gracefully.
5. **CORS & Middleware**: Out-of-the-box support for strict CORS policy, unique execution time profiling, and Request-ID attachment per incoming request.
