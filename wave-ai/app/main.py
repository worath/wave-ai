from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.schemas.project import ProjectRequest
from app.ai.analyzer import analyze_project
from app.pricing.engine import calculate_price
from app.database.database import engine, Base, SessionLocal
from app.database import models
from app.database.models import Service
from app.config import OPENAI_API_KEY


app = FastAPI(
    title="Wave Studio AI",
    description="AI-powered project estimation system for Wave Studio",
    version="0.1.0",
)


# =========================================================
# CORS
# اجازه اتصال سایت WaveStudio به Wave Studio AI
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:80",
        "http://127.0.0.1:8080",
        "https://wavestudio.ir",
        "https://www.wavestudio.ir",
        "https://wavestudiotest.netlify.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Database
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# Root
# =========================================================

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Wave Studio AI is running"
    }


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# Project Analysis
# =========================================================

@app.post("/analyze")
def analyze_project_endpoint(project: ProjectRequest):

    analysis = analyze_project(project.description)

    pricing = calculate_price(analysis)

    return {
        "status": "success",
        "analysis": analysis,
        "pricing": pricing,
    }


# =========================================================
# Services
# =========================================================

@app.get("/services")
def get_services():

    db = SessionLocal()

    services = db.query(Service).all()

    result = [
        {
            "id": service.id,
            "name": service.name,
            "code": service.code,
            "category": service.category,
            "price": service.price,
        }
        for service in services
    ]

    db.close()

    return {
        "services": result
    }


# =========================================================
# Update Service Price
# =========================================================

class ServicePriceUpdate(BaseModel):
    price: int


@app.put("/services/{service_id}")
def update_service_price(
    service_id: int,
    data: ServicePriceUpdate
):

    db = SessionLocal()

    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if service is None:

        db.close()

        return {
            "status": "error",
            "message": "Service not found"
        }

    service.price = data.price

    db.commit()
    db.refresh(service)

    db.close()

    return {
        "status": "success",
        "service": {
            "id": service.id,
            "name": service.name,
            "code": service.code,
            "category": service.category,
            "price": service.price,
        }
    }