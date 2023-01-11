from models.entities import ServiceGame, Plan, BuyPlanGame
from pony.orm import db_session, commit, select
from schemas.iPlan import Buy_plan_transaction_schema

@db_session()
def add_buy_plan_game(new_buy_plan_game: Buy_plan_transaction_schema):
    with db_session:
        try:
            BuyPlanGame(
                id_transaction= new_buy_plan_game.id_transaction,
                user=new_buy_plan_game.username,
                serviceGame=int(new_buy_plan_game.id_service),
                plan=int(new_buy_plan_game.id_plan)
            )
            commit()
        except Exception as e:
            print(e)
            return str(e)

        return "Plan pagado y agregado con exito"

def get_buy_plan_game_from_db(id_transaction: str):
    with db_session:
        try:
            res = BuyPlanGame[id_transaction]
            return res
        except:
            return "id_transaction invalido"

@db_session
def get_games_and_plans_from_db():
    data = {'games': []}
    data['games'] = []
    games = select((sg.name, sg.id_service) for sg in ServiceGame)
    for (nameGame, id_service) in games:
        data['games'].append({
            'name': nameGame,
            'id_service': id_service,
            'plans': []
        })

    plansxgames = select((sg.name, sg.id_service, sg.plans) for sg in ServiceGame)
    for (nameGame, id_service, plan) in plansxgames:
        index = 0
        for i in range(len(data["games"])):
            index = i if (data["games"][i]["id_service"] == id_service) else index
            
        data["games"][index]['plans'].append({
            'id_plan': plan.id_plan,
            'store': plan.store,
            'ram': plan.ram,
            'typeRenewal': plan.typeRenewal,
            'price': plan.price,
            'connection': plan.connection,
            'playerSlot': plan.playerSlot,
            'backupPerWeek': plan.backupPerWeek,
            'dataTransfer': plan.dataTransfer
        })

    return data["games"]

@db_session
def get_plan_from_db(idd_plan: int):
    with db_session:
        try:
            res = Plan.get(id_plan=idd_plan)
            return res
        except:
            return "Invalid plan"