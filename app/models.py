from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.sql import func
from .db import Base

class postdb(Base):
    __tablename__  = 'postdb'

    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable = False)
    content = Column(String,nullable = True)
    is_published = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class userdb(Base):
    __tablename__ = 'userdb'

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    mail = Column(String,nullable=True)
    occupation = Column(String)
    is_active = Column(Boolean,default= True)
    created_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())