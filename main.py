#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.settings import config

from src.api.base import api_router

from src.db.database import engine, get_db_as_obj
from src.db import models

from src.db.crud import create_user, get_user_by_email, get_user_by_username
from src.schemas import UserCreate

from src.core.admin.role_handler import change_user_role


def include_router(app):
    app.include_router(api_router)


def create_tables():
    models.Base.metadata.create_all(bind=engine)


def init_admin() -> int:
    try:
        super_admin_email =  config['SUPER_ADMIN_EMAIL']
        super_admin_username = config['SUPER_ADMIN_USERNAME']
    except Exception:
        return -1

    db = get_db_as_obj()

    if get_user_by_email(db, super_admin_email) or get_user_by_username(db, super_admin_username):
        print("Already created")
        return

    try:
        create_user(db, UserCreate(email=super_admin_email, username=super_admin_username, password="Passw0rd!"))
        db_user = get_user_by_email(db, super_admin_email)
        change_user_role(db, "chief_access", db_user)
    finally:
        db.close()

    return 0


def allow_origins(app):
    origins = [
        "http://localhost",
        "http://localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def start_application():
    app = FastAPI(title="Dashboard", version="/api/v1")
    include_router(app)
    create_tables()
    init_admin()
    allow_origins(app)
    return app


app = start_application()
