#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session

from src import schemas

from src.db import models

from src.db.update import update_element

from src.core.items.status.status_enum import Status


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db_item.item_status = Status.off.value

    update_element(db, db_item)

    return db_item