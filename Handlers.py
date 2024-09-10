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
    id: str
    action: str  # add,remove,update
    categoryid: str
    userid: str


class Publication(BaseModel):
    id: str
    action: str
    categoryid: str
    title: str
    comments: str
