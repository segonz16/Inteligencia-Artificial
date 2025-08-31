from fastapi import FastAPI
from pydantic import BaseModel
import coffee_expert_system as coffee
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserDetails(BaseModel):
    name: str
    prefered_preparation: str
    mood: str

@app.get("/moods")
async def get_moods():
    return {"moods": coffee.moods}

@app.get("/preparations")
async def get_preparations():
    return {"preparations": coffee.preparations}

@app.post("/evaluate")
async def evaluate(user_details: UserDetails):
    return coffee.evaluacion(user_details.name, user_details.prefered_preparation, user_details.mood)
