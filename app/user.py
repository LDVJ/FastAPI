# from fastapi import FastAPI, HTTPException,  status
# from fastapi import Depends
# from pydantic import BaseModel, Field, EmailStr
# from datetime import datetime
# import psycopg
# import time
# from . import models
# from sqlalchemy.orm import Session
# from .db import SessionLocal, engine

# models.userdb.metadata.create_all(bind = engine)

# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class userSchema(BaseModel):
#     name : str
#     createAt : datetime = Field(default_factory=datetime.now)
#     mail : EmailStr
#     occupation : str | None = None
#     is_active: bool | None = True
#     updateAt : datetime | None = None

# # while True:
# #     try:
# #         conn = psycopg.connect(
# #             dbname = 'fastapi',
# #             host = 'localhost',
# #             port = 5432,
# #             user = 'postgres',
# #             password ='ldvj1242210@L'
# #         )
# #         cursor= conn.cursor()
# #         print('DB connect Successfully.')
# #         break

# #     except Exception as error:
# #         print("DB not connected")
# #         print('error: ', error)
# #         time.sleep(2)

# # def checkID(id: int) -> bool:
# #     cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
# #     check = cursor.fetchone()
# #     if check is not None:
# #         return True
# #     return False

# @app.get('/')
# def root():
#     return {'message':"BAckend Running ...."}

# @app.get('/users')
# def get_all_user(db : Session = Depends(get_db)):
#     # cursor.execute('''SELECT * FROM users''')
#     # all_users = cursor.fetchall()
#     all_users = db.query(models.userdb).all()
#     return {'data':all_users}

# @app.get('/users/{id}',status_code=status.HTTP_200_OK)
# def getUser(id: int, db: Session = Depends(get_db)):
#     # if checkID(id):
#     #     cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
#     #     user = cursor.fetchone()
#     check = db.get(models.userdb, id)
#     if  check is None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'Post with id : {id} not found')
#     output = db.query(models.userdb).filter(models.userdb.id == id).first()
#     return {'data':output}

# @app.post('/users',status_code=status.HTTP_201_CREATED)
# def createUser(user: userSchema, db : Session = Depends(get_db)):
#         # cursor.execute('''INSERT INTO users (name, mail,occupation) VALUES (%s,%s,%s)''',
#         #             (user.name,user.mail,user.occupation))
#         # conn.commit()
#         # cursor.execute('''SELECT * FROM users ORDER BY created_at DESC''')
#         # all_user = cursor.fetchall()

#         new_post = models.userdb(**user.model_dump(exclude_unset=True))
#         db.add(new_post)
#         db.commit()
#         db.refresh(new_post)
#         return {'data':new_post}

# @app.put('/users/{id}',status_code=status.HTTP_200_OK)
# def updateUser(id: int,user: userSchema, db : Session = Depends(get_db)):
#     # if checkID(id):
#     #     cursor.execute('''UPDATE users SET name = %s,mail = %s,occupation = %s WHERE id = %s''',
#     #                    (user.name,user.mail,user.occupation,id))
#     #     conn.commit()
#     #     cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
#     #     updated_user = cursor.fetchone()
#     original = db.query(models.userdb).filter(models.userdb.id == id).first()
#     if original is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} not found')

#     update_user = user.model_dump(exlude_unset=True)

#     for key,value in update_user.items():
#         setattr(original,key,value)
    
#     db.commit()
#     db.refresh(original)
#     return {'data':original}
    
                        

# @app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def  deleteUser(id: int, db : Session = Depends(get_db)):
#     # if checkID(id):
#     #     cursor.execute('''DELETE FROM users WHERE id = %s''',(id,))
#     #     conn.commit()
#     #     return 
#     check = db.query(models.userdb).filter(models.userdb.id == id).first()
#     if check is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'No post found with id: {id}')
#     db.delete(check)
#     db.commit()

#     return {'message':"Usesr deleted  successfully"}