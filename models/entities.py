from pony.orm import PrimaryKey, Required, Set
from db.database import db
from datetime import date


class User(db.Entity):
    """Crea la tabla de usuarios.
    """
    __table__ = "User"
    username = PrimaryKey(str, 40)
    password = Required(str, 200)
    email = Required(str, unique=True)
    confirmation_mail = Required(bool)
    validation_code = Required(str, 6)
    
    buyPlansGame = Set("BuyPlanGame")
    buyPlansWeb = Set("BuyPlanWeb")
    buyOffers = Set("Offer", reverse= "buyUsers")

class ServiceGame(db.Entity):
    """Crea la tabla de servicios en venta.
    """ 
    __table__="ServiceGame"
    id_service = PrimaryKey(int, auto=True)
    logo = Required(str, nullable=False)
    ip = Required(str, 20)
    port = Required(int)
    name = Required(str, 40, unique=True)

    plans = Set("Plan", reverse= "servicesGame")
    offers = Set("Offer", reverse= "servicesGame")
    buyPlansGame = Set("BuyPlanGame")

class ServiceWeb(db.Entity):
    """Crea la tabla de servicios en venta.
    """ 
    __table__="ServiceWeb"
    id_service = PrimaryKey(int, auto=True)
    logo = Required(str, nullable=False)
    ip = Required(str, 20)
    port = Required(int)
    benefit = Required(str, 50)

    plans = Set("Plan", reverse= "servicesWeb")
    offers = Set("Offer", reverse= "servicesWeb")
    buyPlansWeb = Set("BuyPlanWeb")

class Plan(db.Entity):
    """Crea la tabla de planes para los servicios ofrecidos.
    """
    __table__="Plan"
    id_plan = PrimaryKey(int, auto=True)
    store = Required(str, 10)
    ram = Required(str, 10)
    typeRenewal = Required(str, 10)
    price = Required(float)
    connection = Required(str, 10)
    playerSlot = Required(str, 20)
    backupPerWeek = Required(int)
    dataTransfer = Required(str, 10)
    Link = Required(str, 400)

    buyUsersGame = Set("BuyPlanGame")
    buyUsersWeb = Set("BuyPlanWeb")
    servicesWeb = Set("ServiceWeb", reverse= "plans")
    servicesGame = Set("ServiceGame", reverse= "plans")

class BuyPlanGame(db.Entity):
    __table__="BuyPlanGame"
    id_transaction = PrimaryKey(str, 100)
    user = Required(User)
    serviceGame = Required(ServiceGame)
    plan = Required(Plan)

class BuyPlanWeb(db.Entity):
    __table__="BuyPlanWeb"
    id_transaction = PrimaryKey(str, 100)
    user = Required(User)
    serviceWeb = Required(ServiceWeb)
    plan = Required(Plan)

class Offer(db.Entity):
    """Crea la tabla de ofertas.
    """
    __table__="Offer"
    id_Offer = PrimaryKey(int, auto=True)
    offerRAM = Required(float)
    date_start = Required(date)
    date_end = Required(date)

    buyUsers = Set("User", reverse= "buyOffers")
    servicesWeb = Set("ServiceWeb", reverse= "offers")
    servicesGame = Set("ServiceGame", reverse= "offers")