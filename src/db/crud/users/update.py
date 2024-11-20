#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session
from re import compile

from src.db.update import update_element

from src.schemas.users import User, UserResetPass

from src.db.crud.users.read import get_user_by_token
from src.db.crud.users.create import create_validation_token

from src.core.auth.auth_handler import get_password_hash
from src.core.mailing.send_mail import send_mail


def update_password(db: Session, db_user: User, new_password: str):
    db_user.hashed_password = get_password_hash(password=new_password)

    update_element(db, db_user)

    return db_user


def reset_user_pass(db: Session, token: str, user_new_pass: UserResetPass):
    db_user = get_user_by_token(db, token)

    if db_user:
        if user_new_pass.password == user_new_pass.confirm_password:
            db_user.validation_token = None
            update_password(db, db_user, new_password=user_new_pass.password)
            return "Your password has been successfully updated."
        else:
            return "Please match password & confirm password."
    return "Link is expired or not exist."


def update_validation_token(db, db_user):
    create_validation_token(db_user)

    update_element(db, db_user)


def is_mail_valid(user_email: str):
    reg = compile('[a-zA-Z0-9.]+@[a-z-]+[.][a-z]{2,4}')

    return True if reg.match(user_email) else False


def update_mail(db, db_user: User, new_mail: str):
    if not is_mail_valid(new_mail):
        return None

    db_user.email = new_mail

    send_mail(None, 'new account mail',
              f'Hi, {db_user.username}, this is a mail to inform that your new mail is: {new_mail}', new_mail)

    update_element(db, db_user)

    return db_user


def verified_user(db: Session, token: str):
    db_user = get_user_by_token(db, token)

    if db_user:
        db_user.validation_token = None
        db_user.is_verified = True

    if not db_user:
        return None

    update_element(db, db_user)

    return db_user


def update_role(db: Session, db_user: User, new_role: str):
    db_user.role = new_role

    update_element(db, db_user)
