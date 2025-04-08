from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,ConfigDict
import uvicorn

app = FastAPI()

data = {
    "email" : "abc@gmail.ru",
    "bio": "1234567890",
    "age": 12,
}
data_wo_age = {
    "email" : "abc@gmail.ru",
    "bio": "1234567890",
    
}

class UserShema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)
    model_config = ConfigDict(extra='forbid')


class UserAgeShema(UserShema):
    age: int = Field(ge = 0, le = 100)

users = []

@app.post("/users/")
def add_user(user : UserShema):
    user.uppend(user)
    return {"ok": True}

@app.get("/users")
def get_users():
    return users