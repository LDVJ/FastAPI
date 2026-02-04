from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from sqlmodel import SQLModel

class postSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: int | None = None

class postResponse(postSchema):
    id: int
    created_at : datetime
    # rating: int 
    model_config = {
        'from_attributes': True
    }

class createUser(BaseModel):
    name : str
    createAt : datetime = Field(default_factory=datetime.now)
    mail : EmailStr
    occupation : str | None = None
    is_active: bool | None = True
    updateAt : datetime | None = None
    password : str 

class UserResponse(BaseModel):
    name : str
    createAt : datetime = Field(default_factory=datetime.now)
    mail : EmailStr
    occupation : str | None = None
    is_active: bool | None = True
    updateAt : datetime | None = None

class updateUser(BaseModel):
    name: str | None =  None
    occupation: str | None = None
    is_active: bool | None = True


# class 