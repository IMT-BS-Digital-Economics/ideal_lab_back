#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 05/07/2022
    About: 

"""
from uuid import UUID

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.core.auth.session_handler import create_session, del_session, cookie

from src.core.auth.auth_handler import authenticate_user
from src.db.database import get_db

router_auth = APIRouter()


@router_auth.post("/signin")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return await create_session(user.username, response)


@router_auth.post("/signout")
async def sign_out(response: Response, session_id: UUID = Depends(cookie)):
    return await del_session(response, session_id)