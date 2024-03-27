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

    while 1:
        db.refresh(project)

        if not project.auto_launch:
            return

        time_to_sleep = (datetime.now() - project.start_time).seconds
        if time_to_sleep > 0:
            sleep(time_to_sleep)

        if p.get_process_status() == Status.running:
            p.turn_off_process()

        p.start_process(project.executable, project.arguments)
