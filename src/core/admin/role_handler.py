#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 04/01/2023
    About: 

"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.crud import update_role
from src.schemas import User

from src.core.admin.role_enum import Roles


def check_role(role):
    try:
        Roles(role)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Role not exist: {role}"
        )


def is_ok_to_execute(current_user: User, user_to_manage: User = None) -> None:
    if user_to_manage and (current_user.username == user_to_manage.username):
        raise HTTPException(
            status_code=403,
            detail="Unauthorized to perform this action: can't manage your own account"
        )

    if current_user.role == "chief_access":
        return

    if current_user.role == "basic_access":
        raise HTTPException(
            status_code=403,
            detail="Unauthorized to perform this action"
        )

    if user_to_manage and (current_user.role == user_to_manage.role or user_to_manage.role == "chief_access"):
        raise HTTPException(
            status_code=403,
            detail=f"Unauthorized to perform this action: this user is an {user_to_manage.role}"
        )


def change_user_role(db: Session, new_role: str, user_to_manage: User):
    check_role(new_role)

    update_role(db, user_to_manage, new_role)

    return user_to_manage

