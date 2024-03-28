
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import  init_db


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=app_lifespan)

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
async def home():
    return {"data": "Hello"}



