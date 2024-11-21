#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 26/03/2024
    About: To handle start of the project if it's actived

"""

from time import sleep

from datetime import datetime

from src.core.projects.handle_process import Status

from src.core.projects.handle_process import ProjectProcess
from src.db.crud import get_project_by_unique_id


def convert_time_to_time_object(start_time):
    dt_obj = datetime.strptime(start_time, '%H:%M')

    dt_obj = datetime.combine(datetime.now().date(), dt_obj.time())

    return dt_obj


def monitoring_time_worker(unique_id: str, user_id, db) -> None:
    """
    Monitoring worker to start the project each day at the same hour
    :param unique_id: unique id of the project
    :param user_id: id of the user
    :param db: database
    :return: Nothing in case of success
    """

    p = ProjectProcess(unique_id)

    project = get_project_by_unique_id(db, unique_id, user_id)

    if not project:
        return None

    while 1:
        db.refresh(project)

        if not project.auto_launch:
            return

        time_to_sleep = (convert_time_to_time_object(project.start_time) - datetime.now()).seconds
        print(time_to_sleep)
        if time_to_sleep > 0:
            sleep(time_to_sleep)

        if p.get_process_status() == Status.running:
            p.turn_off_process()

        p.start_process(project.executable, project.arguments)
