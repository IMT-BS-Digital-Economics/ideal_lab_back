#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 28/03/2024
    About: Update parameters

"""

from enum import Enum

from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.db.crud import update_parameters
from src.schemas.projects import ProjectBase


class Parameter(Enum):
    title = "title"
    description = "description"
    arguments = "arguments"
    start_time = "start_time"


def check_parameter(parameter):
    try:
        Parameter(parameter)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Parameter not found: {parameter}"
        )


def edit_parameter(db: Session, project: ProjectBase, parameter: str, new_value: str):
    update_parameters(db, project, parameter, new_value)
