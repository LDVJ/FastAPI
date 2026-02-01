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
    finally:
        db.close()

class postSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: int | None = None

@app.get('/')
def root():
    return {"Message": 'Welcome to my api'}

@app.get('/sqlalchemy/posts')
def test_posts(db: Session = Depends(get_db)):
    posst = db.query(models.postdb).all()
    return {'data': posst}

@app.post('/sqlalchemy/posts',status_code=status.HTTP_201_CREATED)
def create_post(post: postSchema,db: Session = Depends(get_db)):
    # new_post = models.postdb(title = post.title, content = post.content,is_published = post.is_published)
    new_post = models.postdb(**post.model_dump(exclude_unset=True))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {new_post}

@app.get('/sqlalchemy/posts/{id}',status_code= status.HTTP_200_OK)
def getUser(id: int, db : Session = Depends(get_db)):
    post = db.query(models.postdb).filter(models.postdb.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No Post found with id: {id}')
    return {'data':post}

@app.delete('/sqlalchemy/posts/{id}')
def deletePost(id:int, db : Session = Depends(get_db)):
    output = db.get(models.postdb, id)
    print(output)
    if not output:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id : {id} not found')
    db.delete(output)
    db.commit()
    return 


@app.get('/posts')
def getPost(db: Session = Depends(get_db)):
#     cursor.execute('''SELECT * FROM posts''')
#     post = cursor.fetchall() #fetchaall retrvies all the data from the last executed query
    post = db.query(models.postdb).all()
    return {'data':post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createPost(posts: postSchema, db: Session = Depends(get_db)):
#     cursor.execute('''INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s);''',(posts.title,posts.content,posts.is_published))
#     conn.commit()
#     cursor.execute(''' SELECT * FROM posts ORDER BY crerated_at DESC''')
#     all_posts = cursor.fetchall() 
    new_post = models.postdb(**posts.model_dump(exclude_unset=True))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    all_post = db.query(models.postdb).all()
    return {'data': all_post}

# # retreive a single post dataa based on it's unique identifier (ID)
@app.get("/posts/{id}")
def getPost(id: int, db: Session = Depends(get_db)):
#     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
#     post = cursor.fetchone()
    post = db.query(models.postdb).filter(models.postdb.id == id).first()
    if post is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')
    return {'data':post}

@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def updatepost(id:int, post: postSchema, db: Session = Depends(get_db)):
#     cursor.execute('''UPDATE posts SET title = %s,content = %s,is_published = %s WHERE id = %s ''',(post.title,post.content,post.is_published,id))
#     conn.commit()
#     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
#     update_post = cursor.fetchone()
    orignal = db.query(models.postdb).filter(models.postdb.id == id).first()
    if orignal is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')
    # post = post.model_dump()

    #method 1
    # if post.title is not None:
    #     orignal.title = post.title
    # if post.content is not None:
    #     orignal.content = post.content
    # if post.is_published is not None:
    #     orignal.is_published = post.is_published

    #method 2
    updated_post = post.model_dump(exclude_unset=True)
    for key, value in updated_post.items():
        setattr()
    
    db.commit()
    db.refresh(orignal)
    return {"message":f"Data of the post id: {id} updated successfully.",'data':orignal}

# #Delete Post
@app.delete('/posts/{id}')
def deletepost(id: int,db:Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
    # check = cursor.fetchone()

    #method 1
    check = db.get(models.postdb, id)
    if check is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not post Found with id: {id}")
    db.delete(check)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)




    # cursor.execute('''DELETE FROM posts WHERE id = %s''',(id,)) 
    # conn.commit()
    # cursor.execute('''SELECT * FROM posts''')
    # post = cursor.fetchall()
    # # posts = [dict(row) for row in rows]
    # return {'message':'Post deleted successfully.','data':post}


# @app.put('/sqlalchemy/posts/{id}')
# def update_post(id:int, db:Session = Depends(get_db)):
#     db.u

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

