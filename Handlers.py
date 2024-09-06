from pydantic import BaseModel


class Category(BaseModel):
    action: str  # add,remove,update
    id: str
    name: str


class User(BaseModel):
    action: str  # add,remove,update
    id: str
    username: str
    fullname: str


class Subscription(BaseModel):
    action: str  # add,remove,update
    categoryid: str
    userid: str
