#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.projects.handle_process import Status, load_project_process
from src.core.utils.handle_system_execution import run_command
from src.db.crud.projects.read import get_project_by_unique_id


def del_project(db: Session, unique_id: str, owner_id: int) -> dict:
    project = get_project_by_unique_id(db, unique_id, owner_id)

    if not project:
        raise HTTPException(
            status_code=400,
            detail=f"Project {unique_id} not found"
        )

    project_process = load_project_process(unique_id)

    if project_process.get_process_status() != Status.off:
        raise HTTPException(
            status_code=400,
            detail=f"Project {project.title} must be turned off before deleting it !"
        )

    run_command(f'rm -rf {project_process.folder_path}', shell=True)

    db.delete(project)
    db.commit()

    return {"details": f"Your project {project.title} has been deleted"}
