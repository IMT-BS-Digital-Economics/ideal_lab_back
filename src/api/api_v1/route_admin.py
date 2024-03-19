#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 12/12/2022
    About: 

"""

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends

from src import schemas
from src.db import crud

from src.core.auth.session_handler import verifier, cookie

from src.core.auth.auth_handler import verified_session
from src.db.crud import delete_user

from src.db.database import get_db

from src.core.admin.role_handler import change_user_role, is_ok_to_execute
from src.core.admin.role_enum import Roles

from src.schemas import User, UserMail

router_admin = APIRouter()


@router_admin.post("/create_user", dependencies=[Depends(cookie)])
async def create_user(user: schemas.UserCreate, session_data: schemas.SessionData = Depends(verifier),
                      db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    is_ok_to_execute(db_user)

    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already existed")

    if not crud.is_mail_valid(user.email):
        raise HTTPException(status_code=400, detail="Email not valid")

    crud.create_user(db, user)

    return {"detail": f"An account has been created for {user.username}"}


@router_admin.post("/update_role", dependencies=[Depends(cookie)], response_model=User)
async def update_role(user: schemas.UpdateUserRole, session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    user_to_manage = crud.get_user_by_username(db, user.username)

    is_ok_to_execute(db_user, user_to_manage)

    if not user_to_manage:
        raise HTTPException(status_code=400, detail=f"User not found: {user.username}")

    return change_user_role(db, user.role, user_to_manage)


@router_admin.get("/roles", dependencies=[Depends(cookie)])
async def get_roles(session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    is_ok_to_execute(db_user)

    return [e for e in Roles]


@router_admin.get("/users", dependencies=[Depends(cookie)], response_model=list[User])
async def get_users(session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    is_ok_to_execute(db_user)

    return crud.get_all_users(db)


@router_admin.delete("/user", dependencies=[Depends(cookie)])
async def del_user(user_mail: UserMail, session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    user_to_manage = crud.get_user_by_email(db, user_mail.email)

    is_ok_to_execute(db_user, user_to_manage)

    if not user_to_manage:
        raise HTTPException(status_code=400, detail=f"User not found: {user_mail.email}")

    return delete_user(db, user_to_manage)
