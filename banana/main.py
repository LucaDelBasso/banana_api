import os
import secrets
import motor.motor_asyncio

from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import ConfigDict, BaseModel, Field
from typing import Annotated

app = FastAPI(title="Banana API")

security = HTTPBasic()

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
    

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(os.getenv("SCRAPER_POST_USERNAME", "no_user"), encoding="utf-8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )

    current_password_bytes= credentials.password.encode("utf-8")
    correct_password_bytes = bytes(os.getenv("SCRAPER_POST_PASSWORD", "no_pass"), encoding="utf-8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not(is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
    
    return credentials.username


@app.get("/")
def read_root():
    return {"Hello": "Bananas"}

@app.post("/bananas/")
async def create_banana(banana: Banana, user: Annotated[str, Depends(get_current_username)]):
    banana_dict = banana.model_dump()
    banana_dict.update({"created_at": datetime.now()})
    new_banana = await db["bananas"].insert_one(banana_dict)

    #exclude new ID from response
    created_banana = await db["bananas"].find_one({"_id": new_banana.inserted_id}, {'_id': 0})

    return JSONResponse(content=jsonable_encoder(created_banana), status_code=status.HTTP_201_CREATED)

