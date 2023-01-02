from fastapi import APIRouter, HTTPException,UploadFile
from starlette.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config
from crud.user_services import (
    add_user,
    get_code_for_user,
    update_confirmation
)

from schemas.iuser import User_base, User_login_schema
import shutil
from datetime import datetime
import base64
user_end_points = APIRouter()

MAIL_USERNAME_S = config("MAIL_USERNAME")
MAIL_PASSWORD_S = config("MAIL_PASSWORD")
MAIL_PORT_S = config("MAIL_PORT")
MAIL_SERVER_S = config("MAIL_SERVER")

async def send_confirmation_mail(
        email: str,
        code_validation: str,
        username: str
        ):
    """Envía mail de confirmación.
    Args:
        email (str): email al que enviar la confirmación.
        code_validation (str): código a enviar.
        username (str): usuario al que enviar.
    """
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME_S,
        MAIL_PASSWORD=MAIL_PASSWORD_S,
        MAIL_FROM=email,
        MAIL_PORT=MAIL_PORT_S,
        MAIL_SERVER=MAIL_SERVER_S,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )
    html = open("email.html", "r")
    template = html.read().format(
        user=username,
        end_point_verify=code_validation
        )
    message = MessageSchema(
        subject="Mail de confirmación pyRobots",
        recipients=[email],
        body=template,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


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
    code_validation = get_code_for_user(user_to_add.username)
    if "no existe" in code_validation:
        raise HTTPException(
            status_code=400,
            detail="El usuario " + user_to_add.username + " no existe"
        )
    await send_confirmation_mail(
        user_to_add.email,
        code_validation,
        user_to_add.username
        )
    return {"Status": msg}


@user_end_points.get("/verify")
def user_verification(username: str, code: str):
    """Verificación de usuario
    Args:
        username (str): username
        code (str): token
    Raises:
        HTTPException: 400: el usuario no existe
        HTTPException: 400 el token no es válido
    Returns:
        dict[str, str]: {"Status": msg}
    """
    msg = update_confirmation(username, code)
    if "no existe" in msg:
        raise HTTPException(
            status_code=400,
            detail="El usuario " + username + " no existe"
            )
    if msg == "El codigo de confirmacion no es valido":
        raise HTTPException(
            status_code=400,
            detail=msg
            )
    response = RedirectResponse(url='http://localhost:3000/home/login')
    return response