# from fastapi import Body, Depends, FastAPI, HTTPException, status, Response
# from pydantic import BaseModel
# from random import randrange
# from typing import Dict, List, Any
# import psycopg
# from psycopg.rows import dict_row
# import time
# from sqlalchemy.orm import Session
# from . import models 
# from .db import engine, SessionLocal

# models.Base.metadata.create_all(bind=engine)

# # print(type(models.Base.metadata))

# app = FastAPI()

# #dependency injection
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class postSchema(BaseModel):
#     title: str
#     content: str
#     is_published: bool = True
#     rating: int | None = None

# @app.get('/')
# def root():
#     return {"Message": 'Welcome to my api'}

# @app.get('/sqlalchemy/posts')
# def test_posts(db: Session = Depends(get_db)):
#     posst = db.query(models.postdb).all()
#     return {'data': posst}

# @app.post('/sqlalchemy/posts',status_code=status.HTTP_201_CREATED)
# def create_post(post: postSchema,db: Session = Depends(get_db)):
#     # new_post = models.postdb(title = post.title, content = post.content,is_published = post.is_published)
#     new_post = models.postdb(**post.model_dump(exclude_unset=True))
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {new_post}

# @app.get('/sqlalchemy/posts/{id}',status_code= status.HTTP_200_OK)
# def getUser(id: int, db : Session = Depends(get_db)):
#     post = db.query(models.postdb).filter(models.postdb.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No Post found with id: {id}')
#     return {'data':post}

# @app.delete('/sqlalchemy/posts/{id}')
# def deletePost(id:int, db : Session = Depends(get_db)):
#     output = db.get(models.postdb, id)
#     print(output)
#     if not output:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id : {id} not found')
#     db.delete(output)
#     db.commit()
#     return 


# @app.get('/posts')
# def getPost(db: Session = Depends(get_db)):
# #     cursor.execute('''SELECT * FROM posts''')
# #     post = cursor.fetchall() #fetchaall retrvies all the data from the last executed query
#     post = db.query(models.postdb).all()
#     return {'data':post}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def createPost(posts: postSchema, db: Session = Depends(get_db)):
# #     cursor.execute('''INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s);''',(posts.title,posts.content,posts.is_published))
# #     conn.commit()
# #     cursor.execute(''' SELECT * FROM posts ORDER BY crerated_at DESC''')
# #     all_posts = cursor.fetchall() 
#     new_post = models.postdb(**posts.model_dump(exclude_unset=True))
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     all_post = db.query(models.postdb).all()
#     return {'data': all_post}

# # # retreive a single post dataa based on it's unique identifier (ID)
# @app.get("/posts/{id}")
# def getPost(id: int, db: Session = Depends(get_db)):
# #     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
# #     post = cursor.fetchone()
#     post = db.query(models.postdb).filter(models.postdb.id == id).first()
#     if post is None:    
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')
#     return {'data':post}

# @app.put('/posts/{id}', status_code=status.HTTP_200_OK)
# def updatepost(id:int, post: postSchema, db: Session = Depends(get_db)):
# #     cursor.execute('''UPDATE posts SET title = %s,content = %s,is_published = %s WHERE id = %s ''',(post.title,post.content,post.is_published,id))
# #     conn.commit()
# #     cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
# #     update_post = cursor.fetchone()
#     orignal = db.query(models.postdb).filter(models.postdb.id == id).first()
#     if orignal is None:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id = {id} not found')
#     # post = post.model_dump()

#     #method 1
#     # if post.title is not None:
#     #     orignal.title = post.title
#     # if post.content is not None:
#     #     orignal.content = post.content
#     # if post.is_published is not None:
#     #     orignal.is_published = post.is_published

#     #method 2
#     updated_post = post.model_dump(exclude_unset=True) # it truncates the data to actual daa send by the user
#     for key, value in updated_post.items():
#         setattr(orignal, key, value)  # what it does is that it changes the data in the orignal with the data send by the user and according to the sql it is dirty  but when we apply db.commit() it saves tose changes.
    
#     db.commit()
#     db.refresh(orignal)
#     return {"message":f"Data of the post id: {id} updated successfully.",'data':orignal}

# # #Delete Post
# @app.delete('/posts/{id}')
# def deletepost(id: int,db:Session = Depends(get_db)):
#     # cursor.execute('''SELECT * FROM posts WHERE id = %s''',(id,))
#     # check = cursor.fetchone()

#     #method 1
#     check = db.get(models.postdb, id)
#     if check is None:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not post Found with id: {id}")
#     db.delete(check)
#     db.commit()
#     return HTTPException(status_code=status.HTTP_204_NO_CONTENT)




#     # cursor.execute('''DELETE FROM posts WHERE id = %s''',(id,)) 
#     # conn.commit()
#     # cursor.execute('''SELECT * FROM posts''')
#     # post = cursor.fetchall()
#     # # posts = [dict(row) for row in rows]
#     # return {'message':'Post deleted successfully.','data':post}


# # @app.put('/sqlalchemy/posts/{id}')
# # def update_post(id:int, db:Session = Depends(get_db)):
# #     db.u

# # while True:
# #     try:
# #         conn = psycopg.connect(
# #             dbname="fastapi",
# #             user="postgres",
# #             password="testing details",s
# #             host="localhost",
# #             port=5432,
# #             row_factory = dict_row
# #         )
# #         cursor = conn.cursor()
# #         print('Databasea connection is successfully connect.')
# #         break

# #     except Exception as error:
# #         print("Connecting to Database failed.")
# #         print('Error: ',error)
# #         time.sleep(2)

# # def uniqueID(my_posts: List[Dict[str,Any]]) -> int:
# #     while True:
# #         new_id = randrange(0, 100000)
# #         if not any(p["id"] == new_id for p in my_posts):
# #             return new_id

# # def findIndex(id):
# #     for i,p in enumerate(my_posts):
# #         if p['id'] == id:
# #             return i
# #     return None


from fastapi import FastAPI, HTTPException,  status,Depends
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import psycopg
import time
from . import models
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        print('DB Connected')
        yield db
    finally:
        print('DB Disconnected')
        db.close()

class userSchema(BaseModel):
    name : str
    createAt : datetime = Field(default_factory=datetime.now)
    mail : EmailStr
    occupation : str | None = None
    is_active: bool | None = True
    updateAt : datetime | None = None

# while True:
#     try:
#         conn = psycopg.connect(
#             dbname = 'fastapi',
#             host = 'localhost',
#             port = 5432,
#             user = 'postgres',
#             password ='ldvj1242210@L'
#         )
#         cursor= conn.cursor()
#         print('DB connect Successfully.')
#         break

#     except Exception as error:
#         print("DB not connected")
#         print('error: ', error)
#         time.sleep(2)

# def checkID(id: int) -> bool:
#     cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
#     check = cursor.fetchone()
#     if check is not None:
#         return True
#     return False

@app.get('/')
def root():
    return {'message':"BAckend Running ...."}

@app.get('/users')
def get_all_user(db : Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM users''')
    # all_users = cursor.fetchall()
    all_users = db.query(models.userdb).all()
    return {'data':all_users}

@app.get('/users/{id}',status_code=status.HTTP_200_OK)
def getUser(id: int, db: Session = Depends(get_db)):
    # if checkID(id):
    #     cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
    #     user = cursor.fetchone()
    check = db.get(models.userdb, id)
    if  check is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id : {id} not found')
    output = db.query(models.userdb).filter(models.userdb.id == id).first()
    return {'data':output}

@app.post('/users',status_code=status.HTTP_201_CREATED)
def createUser(user: userSchema, db : Session = Depends(get_db)):
        # cursor.execute('''INSERT INTO users (name, mail,occupation) VALUES (%s,%s,%s)''',
        #             (user.name,user.mail,user.occupation))
        # conn.commit()
        # cursor.execute('''SELECT * FROM users ORDER BY created_at DESC''')
        # all_user = cursor.fetchall()

        new_post = models.userdb(**user.model_dump(exclude_unset=True))
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {'data':new_post}

@app.put('/users/{id}',status_code=status.HTTP_200_OK)
def updateUser(id: int,user: userSchema, db : Session = Depends(get_db)):
    # if checkID(id):
    #     cursor.execute('''UPDATE users SET name = %s,mail = %s,occupation = %s WHERE id = %s''',
    #                    (user.name,user.mail,user.occupation,id))
    #     conn.commit()
    #     cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
    #     updated_user = cursor.fetchone()
    original = db.query(models.userdb).filter(models.userdb.id == id).first()
    if original is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} not found')

    update_user = user.model_dump(exclude_unset=True)

    for key,value in update_user.items():
        setattr(original,key,value)
    db.commit()
    db.refresh(original)
    return {'data':original}
    
                        

@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def  deleteUser(id: int, db : Session = Depends(get_db)):
    # if checkID(id):
    #     cursor.execute('''DELETE FROM users WHERE id = %s''',(id,))
    #     conn.commit()
    #     return 
    check = db.query(models.userdb).filter(models.userdb.id == id).first()
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No post found with id: {id}')
    db.delete(check)
    db.commit()

    return {'message':"Usesr deleted  successfully"}