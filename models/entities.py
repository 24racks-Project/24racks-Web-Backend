from pony.orm import PrimaryKey, Required, Optional, Set
from db.database import db
from datetime import date


class User(db.Entity):
    """Crea la tabla de usuarios.
    """
    __table__ = "users"
    username = PrimaryKey(str, 40)
    password = Required(str, 200)
    email = Required(str, unique=True)
    phone = Optional(str, 13)
    confirmation_mail = Required(bool)
    validation_code = Required(str, 6)
    
    saleServices = Set("SaleService", reverse= "user")
    buyService = Set("BuyService")
    buyOffer = Set("Offer", reverse= "buyUser")
    saleOffer = Set("Offer", reverse= "saleUser")


class SaleService(db.Entity):
    """Crea la tabla de servicios en venta.
    """ 
    __table__="SaleService"
    id_saleService = PrimaryKey(int, auto=True)
    priceStore = Required(float)
    priceRAM = Required(float)
    priceVcpu = Required(float)
    logo = Required(str, nullable=False)
    user = Required(User)

    user = Set("User", reverse= "saleServices")
    buy = Set("BuyService")
    offer = Set("Offer", reverse= "service")


class BuyService(db.Entity):
    """Crea la tabla de servicios comprados.
    """
    __table__="BuyService"
    id_buyService = PrimaryKey(int, auto=True)
    totalStore = Required(float)
    totalRAM = Required(float)
    totalVcpu = Required(float)
    totalAmount = Required(float)
    date_end = Required(date)
    ip = Required(str, 16)
    port = Required(int)

    user = Required(User)
    saleService = Required(SaleService)


class HostingWeb(SaleService):
    """Crea la tabla de HostingWeb que hereda los atributos y 
    relaciones de los servicios en venta (SaleService).
    """
    __table__="HostingWeb"
    benefit = Required(str, 50)


class Game(SaleService):
    """Crea la tabla de juego que hereda los atributos y 
    relaciones de los servicios en venta (SaleService).
    """
    __table__="Game"
    name = Required(str, 40)


class Offer(db.Entity):
    """Crea la tabla de ofertas.
    """
    __table__="Offer"
    id_Offer = PrimaryKey(int, auto=True)
    offerStore = Required(float)
    offerRAM = Required(float)
    offerVcpu = Required(float)
    date_start = Required(date)
    date_end = Required(date)

    buyUser = Set("User", reverse= "buyOffer")
    saleUser = Set("User", reverse= "saleOffer")
    service = Set("SaleService", reverse= "offer")