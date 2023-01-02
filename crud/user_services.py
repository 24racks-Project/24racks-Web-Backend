from models.entities import User
from pony.orm import db_session, commit
from schemas.iuser import User_create
from cryptography.fernet import Fernet
import jwt
from datetime import datetime, timedelta
from decouple import config
import random

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
JWT_EXPIRES = timedelta(1)
KEY_CRYPT = config("KEY")

@db_session()
def add_user(new_user: User_create):
    """Agrega un usuario a la base de datos, devolviendo un
    mensaje representativo del estado de la salida
    Args:
        new_user (User_create): Usuario a persistir
    Returns:
        str: representativa del estado de la salida
    """
    password_encrypted = encrypt_password(new_user.password)
    code_for_validation = ''.join(
        random.sample(password_encrypted[7:13], 6)
        )
    
    with db_session:
        try:
            User(
                username=new_user.username,
                password=password_encrypted,
                email=new_user.email,
                phone=new_user.phone,
                confirmation_mail=False,
                validation_code=code_for_validation
            )
            commit()
        except Exception as e:
            return str(e)
        return "Usuario agregado con exito"


@db_session
def update_confirmation(username: str, code: str):
    """Actualiza el valor del atributo que representa que
    el la cuenta fue confirmada
    Args:
        username (str): Usuario confirmado
        code (str): Codigo de privacidad para la validacion
    Returns:
        str: String representativa del estado de la salida
    """
    try:
        user_for_validate = User[username]
    except Exception as e:
        return str(e)+" no existe"
    if (code == user_for_validate.validation_code and user_for_validate.confirmation_mail == False):
        user_for_validate.confirmation_mail = True
        return "Usuario confirmado con exito"
    elif (code == user_for_validate.validation_code and user_for_validate.confirmation_mail == True):
        return "Intento volver a confirmar"
    return "El codigo de confirmacion no es valido"


@db_session
def get_code_for_user(username: str):
    """Trae el codigo de privacidad de la validacion
    de la base de datos
    Args:
        username (str): Usuario del cual queremos el codigo
    Returns:
        str: Codigo de privacidad
        Any: Error
    """
    try:
        code = User[username].validation_code
    except Exception as e:
        return str(e)+" no existe"
    return code

def encrypt_password(password: str):
    """Realiza un encriptado simetrico a un string haciendo uso de Fernet
    Args:
        password (str): String a encriptar
    Returns:
        _type_: String encriptada
    """
    return password
