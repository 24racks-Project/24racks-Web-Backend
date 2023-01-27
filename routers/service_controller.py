from fastapi import APIRouter, HTTPException
from decouple import config
from crud.user_services import (
    get_user_from_db
)
from crud.plan_services import (
    get_games_and_plans_from_db,
    get_plan_from_db,
    get_buy_plan_game_from_db,
    add_buy_plan_game
)

from schemas.iPlan import Buy_plan_schema, Buy_plan_transaction_schema
import stripe

urlFront = "https://tasty-goat-90.loca.lt/"
urlBack = "https://shan.loca.lt"
service_end_points = APIRouter()

API_KEY = config("API_KEY")

@service_end_points.get("/gamesServer")
async def get_gamesServer():
    return {"games": get_games_and_plans_from_db()}

@service_end_points.post("/buyService")
async def buy_service(credentials: Buy_plan_schema):
    user = get_user_from_db(credentials.token)
    if (user != "token invalido"):
        try:
            plan = get_plan_from_db(credentials.id_plan)
            if (plan != "invalid plan"):
                stripe.api_key= API_KEY
                checkout_session = stripe.checkout.Session.create(
                    line_items = [
                        {
                            'price': plan.Link,
                            'quantity': 1
                        }
                    ],
                    mode="subscription",
                    success_url = urlFront + "saveGameService/" + credentials.username + "/" + credentials.token + "/" + str(credentials.id_service) + "/" + str(credentials.id_plan) + "/{CHECKOUT_SESSION_ID}",
                    cancel_url = urlFront    
                )
                return { "redirect": checkout_session.url}
            else:
                return HTTPException(status_code=400,detail="invalid plan")
        except Exception as e:
            return HTTPException(status_code=400,detail="invalid plan")
    else:
        raise HTTPException(status_code=400,detail="token invalido")

@service_end_points.post("/saveGameService")
async def save_service(credentials: Buy_plan_transaction_schema):
    user = get_user_from_db(credentials.token)
    if (user != "token invalido"):
        transaction = get_buy_plan_game_from_db(credentials.id_transaction)
        if (transaction == "id_transaction invalido"):
            add_buy_plan_game(credentials)
        return {"id_transaction": credentials.id_transaction}
    else:
        raise HTTPException(status_code=400,detail="token invalido")