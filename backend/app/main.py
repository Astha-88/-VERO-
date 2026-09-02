from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.ai_summary import router as ai_summary_router
from app.api.vehicle_report import router as vehicle_report_router
from app.api.incident import router as incident_router
from app.api.ownership import router as ownership_router
from app.api.risk_assessment import router as risk_assessment_router
from app.api.service_record import router as service_record_router
from app.api.vehicle_details import router as vehicle_details_router
from app.api.vehicle_profile import router as vehicle_profile_router
from app.api.vehicles import router as vehicle_router
from app.core import database

app = FastAPI(
    title="VERŌ API",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incident_router)
app.include_router(risk_assessment_router)
app.include_router(service_record_router)
app.include_router(vehicle_router)
app.include_router(vehicle_details_router)
app.include_router(ownership_router)
app.include_router(vehicle_profile_router)
app.include_router(vehicle_report_router)
app.include_router(ai_summary_router)
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
