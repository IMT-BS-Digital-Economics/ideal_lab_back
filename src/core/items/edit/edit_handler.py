#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 07/07/2022
    About: 

"""
import copy

from sqlalchemy.orm import Session
from fastapi import HTTPException
from os import system

from src.schemas import items
from src.core.items.edit.parameter_enum import Parameter
from src.db.crud.items import update_parameters, get_items_by_title
from src.core.items.status.status_enum import Status
from src.core.settings import set_up_dir_name


def check_parameter(parameter):
    try:
        Parameter(parameter)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Parameter not found: {parameter}"
        )


def edit_parameter(db: Session, db_item: items.Item, parameter: str, new_value: str):
    if parameter == "path":
        if db_item.item_status == Status.running.value or db_item.item_status == Status.paused.value:
            raise HTTPException(
                status_code=400,
                detail="You must terminate the current process for this item to modify the path of the executable"
            )

    if parameter == "title":
        if get_items_by_title(db, new_value, db_item.owner_id):
            raise HTTPException(
                status_code=400,
                detail="This title is already taken by another item"
            )

        old_db_item = copy.copy(db_item)

        update_parameters(db, db_item, parameter, new_value)

        system(f'mv {set_up_dir_name(old_db_item)} {set_up_dir_name(db_item, create=False)}')
    else:
        update_parameters(db, db_item, parameter, new_value)

    if parameter != "description":
        return {"detail": f"Item {parameter} has been change to {new_value}"}
    else:
        return {"detail": f"Item {parameter} has been change"}
