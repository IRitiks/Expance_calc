from pydantic import BaseModel

class apiresponse(BaseModel):
    userid:int
    username:str
    content:str
    city:str 