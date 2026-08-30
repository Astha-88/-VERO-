from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.incident import router as incident_router
from app.api.ownership import router as ownership_router
from app.api.vehicle_details import router as vehicle_details_router
from app.api.vehicles import router as vehicle_router
from app.core import database

app = FastAPI(
    title="VERŌ API",
    version="0.1.0",
)
app.include_router(incident_router)
app.include_router(vehicle_router)
app.include_router(vehicle_details_router)
app.include_router(ownership_router)

@app.get("/health/live")
def health_live() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def health_ready() -> JSONResponse:
    if database.check_database_connection():
        return JSONResponse(
            status_code=200,
            content={"status": "ready", "database": "up"},
        )

    return JSONResponse(
        status_code=503,
        content={"status": "not_ready", "database": "down"},
    )
