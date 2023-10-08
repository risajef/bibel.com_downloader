import os
from fastapi import HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = f'sqlite:///{base_dir}/database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
