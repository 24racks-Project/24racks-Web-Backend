from pony.orm import PrimaryKey, Required, Set
from db.database import db
from datetime import date


class User(db.Entity):
    """Crea la tabla de usuarios.
    """
    __table__ = "users"
    username = PrimaryKey(str, 40)
    password = Required(str, 200)
    email = Required(str, unique=True)
    confirmation_mail = Required(bool)
    validation_code = Required(str, 6)
    
    buyPlans = Set("BuyPlan")
    buyOffers = Set("Offer", reverse= "buyUsers")

class ServiceGame(db.Entity):
    """Crea la tabla de servicios en venta.
    """ 
    __table__="Service"
    id_service = PrimaryKey(int, auto=True)
    logo = Required(str, nullable=False)
    ip = Required(str, 20)
    port = Required(int)
    name = Required(str, 40, unique=True)

    plans = Set("Plan", reverse= "servicesGame")
    offers = Set("Offer", reverse= "servicesGame")

class ServiceWeb(db.Entity):
    """Crea la tabla de servicios en venta.
    """ 
    __table__="Service"
    id_service = PrimaryKey(int, auto=True)
    logo = Required(str, nullable=False)
    ip = Required(str, 20)
    port = Required(int)
    benefit = Required(str, 50)

    plans = Set("Plan", reverse= "servicesWeb")
    offers = Set("Offer", reverse= "servicesWeb")



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

    buyUsers = Set("BuyPlan")
    servicesWeb = Set("ServiceWeb", reverse= "plans")
    servicesGame = Set("ServiceGame", reverse= "plans")

class BuyPlan(db.Entity):
    __table__="BuyPlan"
    id_buyPlan = PrimaryKey(int, auto= True)
    user = Required(User)
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