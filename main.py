from fastapi import FastAPI
from db.database import gen_map
from routers.users_controller import user_end_points
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Agregando cors urls
origins = ['https://shan.loca.lt','https://shan.loca.lt:3000', 'https://shan.loca.lt:3000']
# Agregando middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gen_map()
app.include_router(user_end_points)