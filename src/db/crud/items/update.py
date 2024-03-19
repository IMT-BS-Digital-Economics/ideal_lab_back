#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session
from datetime import datetime

from src.db.update import update_element

from src.db.crud.items.read import get_items_by_title

from src.core.items.status.status_enum import Status


def update_item_status(db: Session, title: str, new_status: str, owner_id: int):
    db_item = get_items_by_title(db, title, owner_id)
    db_item.item_status = new_status

    if new_status == Status.running.value:
        db_item.start_time = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

    update_element(db, db_item)


def update_process_id(db: Session, owner_id: int, title: str, process_id: int):
    db_item = get_items_by_title(db, title, owner_id)
    db_item.process_id = process_id

    update_element(db, db_item)


def update_parameters(db: Session, db_item, parameter: str, new_value: str):
    setattr(db_item, f'{parameter}', new_value)

    update_element(db, db_item)

    return {f'{parameter}': eval(f'db_item.{parameter}')}