from fastapi import FastAPI
from .schemas.api_response import apiresponse

app = FastAPI()

@app.get("/users", response_model = apiresponse)
def users():
    response = apiresponse(userid=1, username="Sakshi",content="Food")
    return response

@app.post("/create_user", response_model=apiresponse)
def create_user():
    return apiresponse(userid=2, username="Sachin",content="comedy")


@app.put("/users/{user_id}", response_model=apiresponse)
def update_user(user_id:int):
    return apiresponse(userid=2, username="Shiva",content="rommance")  