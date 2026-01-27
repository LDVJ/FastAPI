from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Any,Dict, List
from random import randrange

app = FastAPI()

class userSchema(BaseModel):
    name : str
    createAt : datetime = Field(default_factory=datetime.now)
    mail : EmailStr
    occupation : str | None = None
    updateAt : datetime | None = None

def findUniqueindex() -> int:
    while True:
        i = randrange(0,10000)
        if not any(u["id"] == i for u in users):
            return i

def uniqueUser(userDict: dict) -> bool:
    return any(u.get("mail") == userDict.get('mail') for u in users)

def findIndex(id: int) -> int | None:
    for i, u in enumerate(users):
        if u['id'] == id:
            return i

users : list[dict[str, Any]] = []

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"data":users}

@app.post('/users')
def createUser(user: userSchema):
    userDict = user.model_dump()
    if uniqueUser(userDict):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'User Already Exists')
    uniqueID = findUniqueindex()
    userDict["id"] = uniqueID
    users.append(userDict)
    return users

@app.get("/users/{id}")
def userinfo(id: int):
    for u in users:
        if(u['id']==id):
            return {'data':u}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user not found with id: {id}')

@app.put('/users/{id}')
def updateUser(id: int, user: userSchema):
    userDict = user.model_dump()
    index = findIndex(id)
    if index is not None:
        old = users[index]
        userDict['id'] = id
        userDict['createAt'] = old['createAt']
        userDict['updateAt'] = datetime.now()
        users[index]= userDict
        return {'data':users[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user found with id: {id}')


@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int):
    index = findIndex(id)
    if index is not None:
        users.pop(index)
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user found with id: {id}')

