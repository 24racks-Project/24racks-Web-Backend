from pydantic import BaseModel, validator

class Buy_plan_schema(BaseModel):
    id_service: int
    id_plan: int
    token: str
    username: str

class Buy_plan_transaction_schema(BaseModel):
    id_plan: str
    id_service: str
    id_transaction: str
    token: str
    username: str

