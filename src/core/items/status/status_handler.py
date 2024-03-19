#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 06/07/2022
    About: 

"""
from os import kill, system, path
from psutil import pid_exists
from signal import SIGSTOP, SIGCONT, SIGTERM

from src.schemas import items
from src.db.crud.items import update_process_id
from src.core.items.status.status_enum import Status
from src.core.settings import set_up_dir_name


def check_status(item_status) -> str:
    try:
        Status(item_status)
        return item_status
    except Exception:
        return None


def running(db, owner_id: int, db_item: items.Item):
    if db_item.item_status == Status.paused.value and pid_exists(db_item.process_id):
        kill(db_item.process_id, SIGCONT)

        return "Item has been restarted"

    if db_item.item_status == Status.running.value:
        return "Item is already running..."

    dir_name = set_up_dir_name(db_item)


    system(f'cd {db_item.path}')
    system(f'source bin/activate')
    system(f'python3 -u {db_item.path} {" ".join(db_item.arguments)}> {dir_name}/out.txt 2> {dir_name}/err.txt & echo $! > {dir_name}/pid')

    with open(f'{dir_name}/pid', 'r') as f:
        update_process_id(db, owner_id, db_item.title, int(f.readline().strip()))

    system(f'rm {dir_name}/pid')

    return "Item is running..."


def paused(db, owner_id: int, db_item: items.Item):
    if not db_item.process_id:
        return "Item hasn't been start yet"

    if pid_exists(db_item.process_id):
        kill(db_item.process_id, SIGSTOP)

    return "Item is in paused..."


def off(db, owner_id: int, db_item: items.Item):
    if not db_item.process_id:
        return "Item hasn't been start yet"

    if pid_exists(db_item.process_id):
        kill(db_item.process_id, SIGTERM)

    update_process_id(db, owner_id, db_item.title, None)

    return "Item is turning off..."


def unreachable(db, owner_id: int, db_item: items.Item):
    pass


def action(db, db_user, db_item: items.Item, item_status: str) -> int:
    return eval('{func_name}(db, db_user.id, db_item)'.format(func_name=item_status))
