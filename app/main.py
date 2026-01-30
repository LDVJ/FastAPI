from fastapi import Body, Depends, FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
from typing import Dict, List, Any
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models 
from .db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

# print(type(models.Base.metadata))

app = FastAPI()

#dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

class postSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: int | None = None

@app.get('/')
def root():
    return {"Message": 'Welcome to my api'}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posst = db.query(models.postdb)
    print(posst)
    return {'data': 'Success'}

# while True:
#     try:
#         conn = psycopg.connect(
#             dbname="fastapi",
#             user="postgres",
#             password="testing details",s
#             host="localhost",
#             port=5432,
#             row_factory = dict_row
#         )
#         cursor = conn.cursor()
#         print('Databasea connection is successfully connect.')
#         break

#     except Exception as error:
#         print("Connecting to Database failed.")
#         print('Error: ',error)
#         time.sleep(2)

# def uniqueID(my_posts: List[Dict[str,Any]]) -> int:
#     while True:
#         new_id = randrange(0, 100000)
#         if not any(p["id"] == new_id for p in my_posts):
#             return new_id

# def findIndex(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
#     return None



# @app.get('/posts')
# def getPost():
#     cursor.execute('''SELECT * FROM posts''')
#     post = cursor.fetchall() #fetchaall retrvies all the data from the last executed query
#     return {'data':post}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def createPost(posts: postSchema):
#     cursor.execute('''INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s);''',(posts.title,posts.content,posts.is_published))
#     conn.commit()
#     cursor.execute(''' SELECT * FROM posts ORDER BY crerated_at DESC''')
#     all_posts = cursor.fetchall() 
#     return {'data': all_posts}

# # retreive a single post dataa based on it's unique identifier (ID)
# @app.get("/posts/{id}")
# def getPost(id: int):
#     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
#     post = cursor.fetchone()
#     if post is not None:    
#         return {'data': post}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')

# @app.put('/posts/{id}', status_code=status.HTTP_200_OK)
# def updatepost(id:int, post: postSchema):
#     cursor.execute('''UPDATE posts SET title = %s,content = %s,is_published = %s WHERE id = %s ''',(post.title,post.content,post.is_published,id))
#     conn.commit()
#     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
#     update_post = cursor.fetchone()
#     if update_post is not None:
#         return {"message":f"Data of the post id: {id} updated successfully.",'data':update_post}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')

# #Delete Post
# @app.delete('/posts/{id}')
# def deletepost(id: int):
#     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
#     check = cursor.fetchone()
#     if check is not None:
#         cursor.execute('''DELETE FROM posts WHERE id = %s''',(id,)) 
#         conn.commit()
#         cursor.execute('''SELECT * FROM posts''')
#         post = cursor.fetchall()
#         # posts = [dict(row) for row in rows]
#         return {'message':'Post deleted successfully.','data':post}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not post Found with id: {id}")
