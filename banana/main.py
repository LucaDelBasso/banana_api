import os
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field
import motor.motor_asyncio

app = FastAPI(title="Banana API")
MONGO_URI = f'mongodb://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@banana_db:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[os.getenv('DB')]

class Banana(BaseModel):
    origin: str = Field(...)
    publication_date: datetime = Field(...)
    price: float = Field(...)
    units: str = Field(...)

    model_config = {
        "populate_by_name":True,
        "arbitrary_types_allowed":True,
        "json_schema_extra":{
            "examples": [
                {
                    "origin": "Belize",
                    "publication_date": datetime(1998,12,4),
                    "price": 0.98,
                    "units": "£/kg"
                }
            ]
        }
    }
    

@app.get("/")
def read_root():
    return {"Hello": "Bananas"}

@app.post("/bananas/")
async def create_banana(banana: Banana):
    banana_dict = banana.model_dump()
    banana_dict.update({"created_at": datetime.now()})
    new_banana = await db["bananas"].insert_one(banana_dict)
    created_banana = await db["bananas"].find_one({"_id": new_banana.inserted_id})

    return JSONResponse(content=jsonable_encoder(created_banana), status_code=status.HTTP_201_CREATED)