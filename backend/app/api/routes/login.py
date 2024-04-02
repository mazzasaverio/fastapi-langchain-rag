from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import user_crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
    verify_password_reset_token,
)
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user_model import Message, NewPassword, Token, UserOut
from app.core.config import logger

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    logger.info(f"User {user} logged in")
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=100000)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
