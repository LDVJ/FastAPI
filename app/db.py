from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALACHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ipaddress-hostname>/<databasename>'
SQLALACHEMY_DATABASE_URL = 'postgres://postgres:<password>@localhost/fastapi'

engine = create_engine(SQLALACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False,
                            autoflush=False,
                            bind=engine)
Base = declarative_base()
