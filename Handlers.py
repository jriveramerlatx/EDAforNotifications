from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str


class User(BaseModel):
    id: str
    username: str
    fullname: str


class Subscription(BaseModel):
    action: str  # add,remove
    categoryid: str
    userid: str
