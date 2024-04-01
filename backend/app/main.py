from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings

from typing import Dict

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/metrics")
def metrics():
    return {"message": "Metrics endpoint"}


@app.get("/")
async def root() -> Dict[str, str]:
    """An example "Hello world" FastAPI route."""
    return {"message": "FastAPI backend"}


app.include_router(api_router, prefix=settings.API_V1_STR)
