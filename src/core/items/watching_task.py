#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 08/07/2022
    About: 

"""

from time import sleep
from os import path, system
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.core.items.status.status_enum import Status
from src.core.items.status.status_handler import off, running
from src.core.settings import set_up_dir_name

from src.db.crud.items import get_items_by_title, update_item_status
from src.db.crud.reports import create_report

from src.schemas.reports import ReportBase


def get_next_day(current_time, timing):
    day = current_time + timedelta(days=1)
    return datetime(year=day.year, month=day.month, day=day.day, hour=int(timing[0]), minute=int(timing[1]))


def item_time_handling(db, db_item, next_day):
    current_time = datetime.now()

    timing = db_item.time_to_start.split(':')

    if next_day is None:
        next_day = get_next_day(current_time, timing)

    if next_day is not None and next_day.year == current_time.year and next_day.month == current_time.month and next_day.day == current_time.day:
        if 0 <= (next_day - current_time).total_seconds() <= 60:
            off(db, db_item.owner_id, db_item)
            running(db, db_item.owner_id, db_item)
            next_day = get_next_day(current_time, timing)

    return next_day


def watching_item_run(db: Session, item_title, item_owner_id):
    db_item = get_items_by_title(db, item_title, item_owner_id)

    dir_path: str = f'{set_up_dir_name(db_item, create=False)}'

    fp_err: str = f'{dir_path}/err.txt'

    fp_out: str = f'{dir_path}/out.txt'

    err_time: datetime = None

    next_day = None

    while 1:
        db_item = get_items_by_title(db, item_title, item_owner_id)

        db.refresh(db_item)

        if db_item.start_time:
            if db_item.item_status == Status.off.value or db_item.item_status == Status.paused.value:
                update_item_status(db, db_item.title, Status.off.value, db_item.owner_id)
                break

        if path.isfile(fp_err):
            with open(fp_err, 'r') as f:
                traceback = f.read().lower()
                if 'traceback' in traceback and datetime.fromtimestamp(
                        path.getmtime(fp_err)) != datetime.now() and db_item.item_status != Status.unreachable.value:
                    err_time = datetime.now()
                    update_item_status(db, db_item.title, Status.unreachable.value, db_item.owner_id)
                    create_report(db, ReportBase.parse_obj(
                        {"time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"), "traceback": traceback}), db_item.id)
                    system(f'rm -rf {fp_err}')

        if path.isfile(fp_out):
            if err_time is not None and db_item.item_status == Status.unreachable.value and datetime.fromtimestamp(
                    path.getmtime(fp_out)) > err_time:
                update_item_status(db, db_item.title, Status.running.value, db_item.owner_id)

        next_day = item_time_handling(db, db_item, next_day)

        sleep(1)
