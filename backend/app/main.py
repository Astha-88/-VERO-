from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core import database

app = FastAPI(
    title="VERŌ API",
    version="0.1.0",
)


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
