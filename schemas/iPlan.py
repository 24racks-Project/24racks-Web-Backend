from pydantic import BaseModel, validator
from typing import Optional
import re

class Plan_base(BaseModel):
    id_plan: int
    price: float

class Buy_plan_schema(BaseModel):
    id_service: int
    id_plan: int
    price: float
    token: str
    username: str

