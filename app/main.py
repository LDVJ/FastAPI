from fastapi import FastAPI
from . import models 
from .db import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

# print(type(models.Base.metadata))

app = FastAPI()

@app.get("/")
def landing():
    return {'message':'WElcome to fasapi '}

app.include_router(post.router)
app.include_router(user.router)
