from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALACHEMY_DATABASE_URL = 'postgresql+psycopg://<username>:<password>@<ipaddress-hostname>/<databasename>'
SQLALACHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:ldvj1242210%40L@localhost/fastapi'
# SQLALACHEMY_DATABASE_URL = 'postgres://postgres:<password>@localhost/fastapi'

engine = create_engine(SQLALACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False,
                            autoflush=False,
                            bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print('DB Connected')
        yield db
    finally:
        print('DB Disconnected')
        db.close()