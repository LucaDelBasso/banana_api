import os
from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel, Field
import motor.motor_asyncio

app = FastAPI(title="Banana API")
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:27017')
db = client[os.environ('MONGO_INITDB_DATABASE')]

class Banana(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    origin: str = Field(...)
    date: date = Field(...)
    price: float = Field(...)
    units: str = Field(...)


@app.get("/")
def read_root():
    return {"Hello": "Bananas"}

