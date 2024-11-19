#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from src.core.auth.auth_handler import verified_session
from src.core.mailing.send_mail import send_verification_mail, send_reset_password_mail, send_new_email
from src.db.crud import verified_user, update_validation_token, reset_user_pass, update_mail, delete_user, \
    get_user_by_email
from src.schemas.users import SessionData, User, UserResetPass, UserMail
from src.core.auth.session_handler import verifier, cookie
from src.db.database import get_db

router_user = APIRouter()


@router_user.get('/me', dependencies=[Depends(cookie)], response_model=User)
async def me(session_data: SessionData = Depends(verifier), db: Session = Depends(get_db)):
    return verified_session(db, session_data)


@router_user.get('/verified/{token}')
async def verified(token: str, db: Session = Depends(get_db)):
    db_user = verified_user(db, token)

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="This link has expired"
        )

    return {"message": f"Welcome {db_user.username} ! You are now an approved user !"}


@router_user.post('/verify', dependencies=[Depends(cookie)])
async def verify(session_data: SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data, to_verify=True)

    if db_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="User has been already verified"
        )

    send_verification_mail(db_user)

    return {"message": "An email has been sent to you"}


@router_user.post('/forgot_password')
async def forgot_password(email: UserMail, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email.email)

    if not db_user:
        return {"message": "An email has been sent to you in order to reset your password"}

    update_validation_token(db, db_user)

    send_reset_password_mail(db_user)

    return {"message": "An email has been sent to you in order to reset your password"}


@router_user.post('/reset_password/{token}')
async def reset_password(token: str, user_new_pass: UserResetPass, db: Session = Depends(get_db)):
    if reset_user_pass(db, token, user_new_pass) is None:
        raise HTTPException(
            status_code=400,
            detail="This is a dead link"
        )

    return {"message": "Your password has been changed !"}


@router_user.post('/reset_email', dependencies=[Depends(cookie)])
async def reset_mail(email: UserMail, session_data: SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    result = update_mail(db, db_user, email.email)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect mail provided: {email.email}"
        )
    
    send_new_email(db_user)

    return {"message": f"You have changed your email to {result.email}"}


@router_user.delete('/', dependencies=[Depends(cookie)])
async def del_user(session_data: SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    return delete_user(db, db_user)
