from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StringConstraints

from app.db import add_check, get_check_counts, init_db
from app.services.availability import calculate_availability

# Database configuration
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "checks.db"


# Request validation
ServiceName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class HealthCheckCreate(BaseModel):
    service: ServiceName
    success: bool


# Application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(DB_PATH)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/availability")
def get_availability(successful: int, total: int):
    try:
        availability = calculate_availability(successful, total)
        return {"availability": availability}

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/checks", status_code=201)
def create_health_check(check: HealthCheckCreate):
    add_check(
        DB_PATH,
        check.service,
        check.success,
    )

    return {
        "message": "Health check recorded",
        "service": check.service,
    }


@app.get("/services/{service}/availability")
def get_service_availability(service: str):
    successful, total = get_check_counts(DB_PATH, service)

    if total == 0:
        raise HTTPException(
            status_code=404,
            detail="No health checks found for this service",
        )

    availability = calculate_availability(successful, total)

    return {
        "service": service,
        "successful_checks": successful,
        "total_checks": total,
        "availability": availability,
    }
