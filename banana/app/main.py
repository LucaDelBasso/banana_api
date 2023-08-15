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
bananas = db["bananas"]
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
    '''
    A HTTP Auth method that uses 'secrets' module, prevents certain attacks.
    probably overkill given this project.

    read more here: https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#check-the-username
    '''
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
    '''
        Takes JSON data for a banana and writes it to the mongoDB Collection if it is the correct user.
    '''
    banana_dict = banana.model_dump()
    banana_dict.update({"created_at": datetime.now()})
    new_banana = await bananas.insert_one(banana_dict)

    #exclude new ID from response
    created_banana = await bananas.find_one({"_id": new_banana.inserted_id}, {'_id': 0})

    return JSONResponse(content=jsonable_encoder(created_banana), status_code=status.HTTP_201_CREATED)


@app.get("/bananas/")
async def get_bananas(
    origin: str | None = None, skip: int = 0, limit: int = 1000, sort_by: str = 'publication_date', sort_asc: int = 1
):
    '''
        Returns Bananas which can optionally be filtered on by origin.
    '''

    origin_search = {}
    if origin:
        origin_search = {'origin': origin}

    cursor = bananas.find(origin_search,{'_id': 0}).sort(sort_by,sort_asc).skip(skip).limit(limit)

    total_count = await bananas.count_documents(origin_search)
    set_count = await bananas.count_documents(origin_search,skip=skip,limit=limit)

    retrieved_bananas = await cursor.to_list(length=limit)
    
    headers = {"total-banana-count": str(total_count), 'returned-banana-count': str(set_count)}

    return JSONResponse(content=jsonable_encoder(retrieved_bananas),headers=headers, status_code=status.HTTP_200_OK)

