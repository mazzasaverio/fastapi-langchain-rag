from fastapi import APIRouter

from app.api.routes import qa, login

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    qa.router,
    prefix="/qa",
    tags=["qa"],
)
