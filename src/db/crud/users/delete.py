#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session

from src.db.models.users import User


def delete_user(db: Session, db_user: User) -> dict:
    db.delete(db_user)
    db.commit()

    return {"detail": 'Success'}