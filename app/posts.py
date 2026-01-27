from fastapi import Body, FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
from typing import Dict, List, Any
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class postSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: int | None = None

while True:
    try:
        conn = psycopg.connect(
            dbname="fastapi",
            user="postgres",
            password="testing details",
            host="localhost",
            port=5432,
            row_factory = dict_row
        )
        cursor = conn.cursor()
        print('Databasea connection is successfully connect.')
        break

    except Exception as error:
        print("Connecting to Database failed.")
        print('Error: ',error)
        time.sleep(2)

def uniqueID(my_posts: List[Dict[str,Any]]) -> int:
    while True:
        new_id = randrange(0, 100000)
        if not any(p["id"] == new_id for p in my_posts):
            return new_id

def findIndex(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

my_posts = [{"title":"title of the post 1","content": "content of the post 1","is_published":True,"rating":4,"id":1},
            {"title":"title of the post 2","content": "content of the post 2","is_published":False,"rating":2,"id":2}]

@app.get('/')
def root():
    return {"Message": 'Welcome to my api'}

@app.get('/posts')
def getPost():
    cursor.execute('''SELECT * FROM posts''')
    post = cursor.fetchall() #fetchaall retrvies all the data from the last executed query
    return {'data':post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createPost(posts: postSchema):
    cursor.execute('''INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s);''',(posts.title,posts.content,posts.is_published))
    conn.commit()
    cursor.execute(''' SELECT * FROM posts''')
    all_posts = cursor.fetchall() 
    return {'data': all_posts}

# retreive a single post dataa based on it's unique identifier (ID)
@app.get("/posts/{id}")
def getPost(id: int):
    for p in my_posts:
        if p["id"] == id:
            return {"data": p}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')
# Path Operation

@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def updatepost(id:int, post: postSchema):
    index = findIndex(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not post Found with id: {id}")
    postDict = post.model_dump()
    postDict['id'] = id
    my_posts[index] = post
    return {"message":f"Data of the post id: {id} updated successfully."}

#Delete Post
@app.delete('/posts/{id}')
def deletepost(id: int):
    index = findIndex(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not post Found with id: {id}")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
