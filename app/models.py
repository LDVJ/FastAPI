from sqlalchemy import Column, Integer, String, Boolean,TIMESTAMP
from .db import Base

class postdb(Base):
    __tablename__  = 'postdb'

    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable = False)
    content = Column(String,nullable = True)
    is_published = Column(Boolean,nullable=False,default=True)
    creted_at = Column()