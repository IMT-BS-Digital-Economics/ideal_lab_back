#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 17/06/2022
    About: Create the DataBase Class & Engine

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from src.core.settings import config

SQLALCHEMY_DATABASE_URL = f"sqlite:///{config['DB_PATH']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_db_as_obj():
    return SessionLocal()
