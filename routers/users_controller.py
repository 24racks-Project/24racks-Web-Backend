from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from decouple import config
from crud.user_services import (
    add_user,
    get_code_for_user,
    update_confirmation,
    search_user,
    decrypt_password,
    sign_JWT,
    get_user_from_db,
    set_user_password
)

from schemas.iuser import User_base, User_login_schema, User_data_schema, User_new_passsword_schema
import smtplib 
from email.message import EmailMessage

urlFront = "https://tasty-goat-90.loca.lt/"
urlBack = "https://shan.loca.lt"
user_end_points = APIRouter()

MAIL_USERNAME_S = config("MAIL_USERNAME")
MAIL_PASSWORD_S = config("MAIL_PASSWORD")
MAIL_PORT_S = config("MAIL_PORT")
MAIL_SERVER_S = config("MAIL_SERVER")
MAIL = config("MAIL")
API_KEY = config("API_KEY")

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
    message = EmailMessage()
    message['Subject'] = "Mail de confirmación 24racks" 
    message['From'] = MAIL 
    message['To'] = email
    
    html = open("email.html", "r")
    template = html.read().format( user=username, end_point_verify=code_validation, loginPage= urlBack+"/verify?username="+username+"&code="+code_validation )

    message.set_content(template, subtype='html')
    server = smtplib.SMTP_SSL(MAIL_SERVER_S, MAIL_PORT_S)
    server.ehlo() 
    server.set_debuglevel(1)
    server.login(MAIL, MAIL_PASSWORD_S) 
    server.send_message(message) 
    server.quit()

    


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
    response = RedirectResponse(url= urlFront+'/signUp')
    return response

@user_end_points.post("/login")
async def user_login(credentials: User_login_schema):
    """Iniciar Sesión.
    Args:
        credentials (User_login_schema): credenciales, username y contraseña.
    Raises:
        HTTPException: 400: el usuario no existe.
        HTTPException: 400: contraseña incorrecta.
        HTTPException: 400: email no verificado.
    Returns:
        dict[str:str]: {"token": response}
    """
    data = search_user(credentials.username)

    if data is None:
        raise HTTPException(status_code=400, detail="no existe el usuario")
    else:
        pass_decrypt = decrypt_password(data.password)
        mail_is_verificated = data.confirmation_mail
        password_is_correct = credentials.password == pass_decrypt

        if not password_is_correct:
            raise HTTPException( status_code=400, detail="contraseña incorrecta" )
        elif not mail_is_verificated:
            raise HTTPException( status_code=400, detail="email no verificado" )
        else:
            response = sign_JWT(credentials.username)
            return {
                "token": response, 
                "username": credentials.username
            }

@user_end_points.get("/dataUser")
async def user_data(credentials: User_data_schema):
    user = get_user_from_db(credentials.token)
    if (user != "token invalido"):        
        return {
            "username":user.username,
            "email":user.email,
            "phone":user.phone
        }
    else:
        raise HTTPException(status_code=400,detail="token invalido")


@user_end_points.post("/newPassword")
async def user_data(credentials: User_new_passsword_schema):
    user = get_user_from_db(credentials.token)
    if (user != "token invalido"):
        if (decrypt_password(user.password) == credentials.currentPassword):
            return set_user_password(credentials.token, credentials.newPassword)
        else:
            raise HTTPException(status_code=400,detail="contraseña actual incorrecta")
    else:
        raise HTTPException(status_code=400,detail="token invalido")
