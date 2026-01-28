from fastapi import FastAPI, HTTPException,  status
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import psycopg
import time


app = FastAPI()

class userSchema(BaseModel):
    name : str
    createAt : datetime = Field(default_factory=datetime.now)
    mail : EmailStr
    occupation : str | None = None
    is_active: bool | None = True
    # updateAt : datetime | None = None

while True:
    try:
        conn = psycopg.connect(
            dbname = 'fastapi',
            host = 'localhost',
            port = 5432,
            user = 'postgres',
            password ='ldvj1242210@L'
        )
        cursor= conn.cursor()
        print('DB connect Successfully.')
        break

    except Exception as error:
        print("DB not connected")
        print('error: ', error)
        time.sleep(2)

def checkID(id: int) -> bool:
    cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
    check = cursor.fetchone()
    if check is not None:
        return True
    return False

@app.get('/')
def root():
    return {'message':"BAckend Running ...."}

@app.get('/users')
def get_all_user():
    cursor.execute('''SELECT * FROM users''')
    all_users = cursor.fetchall()
    return {'data':all_users}

@app.get('/users/{id}',status_code=status.HTTP_200_OK)
def getUser(id: int):
    if checkID(id):
        cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
        user = cursor.fetchone()
        return {'data':user}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id : {id} not found')

@app.post('/users',status_code=status.HTTP_201_CREATED)
def createUser(user: userSchema):
    
        cursor.execute('''INSERT INTO users (name, mail,occupation) VALUES (%s,%s,%s)''',
                    (user.name,user.mail,user.occupation))
        conn.commit()
        cursor.execute('''SELECT * FROM users ORDER BY created_at DESC''')
        all_user = cursor.fetchall()
        return {'data':all_user}

@app.put('/users/{id}',status_code=status.HTTP_200_OK)
def updateUser(id: int,user: userSchema):
    if checkID(id):
        cursor.execute('''UPDATE users SET name = %s,mail = %s,occupation = %s WHERE id = %s''',
                       (user.name,user.mail,user.occupation,id))
        conn.commit()
        cursor.execute('''SELECT * FROM users WHERE id = %s''',(id,))
        updated_user = cursor.fetchone()
        return {'data':updated_user}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id: {id} not found')

@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def  deleteUser(id: int):
    if checkID(id):
        cursor.execute('''DELETE FROM users WHERE id = %s''',(id,))
        conn.commit()
        return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No post found with id: {id}')