from fastapi import APIRouter, HTTPException,UploadFile
from starlette.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config
from crud.user_services import (
    add_user,
    get_code_for_user
)

from schemas.iuser import User_base, User_login_schema
import shutil
from datetime import datetime
import base64
user_end_points = APIRouter()


@user_end_points.post("/register")
async def user_register(user_to_add: User_base):
    """Registrar usuario
    Args:
        user_to_add (User_base): usuario a registrar
    Raises:
        HTTPException: IntegrityError:409, el usuario ya existe.
        HTTPException: IntegrityError:409, el email ya existe.
        HTTPException: 400: el usuario no existe.
    Returns:
        dict[str, str]: {"Status": msg}
    """
    msg = add_user(new_user=user_to_add)
    if ('IntegrityError' in msg and 'username' in msg):
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario ya existe"
            )
    if ('IntegrityError' in msg and 'email' in msg):
        raise HTTPException(
            status_code=409,
            detail="El email ya existe"
            )
    return {"Status": msg}
