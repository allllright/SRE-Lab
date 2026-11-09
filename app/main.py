from fastapi import FastAPI, HTTPException

from app.services.availability import calculate_availability

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/availability")
def get_availability(successful: int, total: int):
    try:
        availability = calculate_availability(successful, total)
        return {"availability": availability}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
