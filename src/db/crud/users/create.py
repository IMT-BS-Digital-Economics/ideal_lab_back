#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session
from datetime import timedelta

from src.schemas.users import UserCreate

from src.db.update import update_element
from src.db.models.users import User

from src.core.settings import config
from src.core.auth.auth_handler import create_access_token, get_password_hash
from src.core.settings import config
from src.core.mailing.send_mail import send_verification_mail


def create_validation_token(db_user):
    access_token_expires = timedelta(minutes=int(config['ACCESS_TOKEN_EXPIRE_MINUTES']))
    db_user.validation_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password)

    create_validation_token(db_user)

    update_element(db, db_user)

    send_verification_mail(db_user)

    return db_user