from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class postSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: int | None = None


class userSchema(BaseModel):
    name : str
    createAt : datetime = Field(default_factory=datetime.now)
    mail : EmailStr
    occupation : str | None = None
    is_active: bool | None = True
    updateAt : datetime | None = None