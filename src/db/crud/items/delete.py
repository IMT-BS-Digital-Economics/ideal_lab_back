#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from fastapi import HTTPException
from os import system

from sqlalchemy.orm import Session

from src.db.crud.items.read import get_items_by_id

from src.core.settings import set_up_dir_name

from src.core.items.status.status_enum import Status


def del_items(db: Session, item_title: str, owner_id: int) -> dict:
    item = get_items_by_id(db, item_title, owner_id)

    if not item:
        raise HTTPException(
            status_code=400,
            detail="Item not found"
        )

    if item.item_status != Status.off.value:
        raise HTTPException(
            status_code=400,
            detail="Item must be turned off before deleting it !"
        )

    system(f'rm -rf {set_up_dir_name(item)}')

    db.delete(item)
    db.commit()

    return {"details": "Your item has been deleted"}
