from fastapi import FastAPI

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Hello from venv"}

@app.get('/about')
def about():
    return {"Message": "My name is Akshay Chaudhary, I'm a software engineer"}


@app.get('/users')
def users():
    users = ["Akshay", "Vishal", "kahshdf"]

    return {
        "users": users
    }

@app.get('/user/{user_id}')
def get_user(user_id: int):
    return {"user": user_id}

@app.get('/params')
def params(name: str = None):
    return {"name": name}


# post apis start here

@app.post('/addUser')
def addUser(data: User):
    return {
        "message": "User data",
        "data": data
    }