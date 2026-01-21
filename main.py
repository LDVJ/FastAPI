from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange
from typing import Dict, List, Any

app = FastAPI()

class postSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


def uniqueID(my_posts: List[Dict[str,Any]]) -> int:
    while True:
        new_id = randrange(0, 100000)
        if not any(p["id"] == new_id for p in my_posts):
            return new_id



my_posts = [{"title":"title of the post 1","content": "content of the post 1","published":True,"rating":4,"id":1},{"title":"title of the post 2","content": "content of the post 2","published":False,"rating":2,"id":2}]

@app.post('/posts')
def createPost(posts: postSchema):
    data = posts.model_dump()
    new_id = uniqueID(my_posts)
    data["id"] = new_id 
    my_posts.append(data)
    return {'data': my_posts, "orignal": posts}


# retreive a single post dataa based on it's unique identifier (ID)
@app.get("/posts/{id}")
def getPost(id):
    print(id)
    return {"data":"ID rertrived successfully"}

# Path Operation
@app.get('/')
def root():
    return {"Message": 'Welcome to my api'}

@app.get('/posts')
def getPost():
    post = {"data":my_posts}
    return post

# @app.post('/createPost')
# def create_Post(payload: dict = Body(...)):
#     return {"new_post": f'post with title {payload['title']} is created'}
# title str, content str, category, published bool