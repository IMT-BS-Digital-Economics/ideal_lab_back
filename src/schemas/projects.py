#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 19/03/2024
    About: Schema for projects

"""

from datetime import datetime

from typing import Union, Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    unique_id: str
    title: str
    description: Union[str, None] = None
    status: str
    arguments: list = []
    executable: str
    start_time: datetime
    auto_launch: bool = False


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]
    repository: str
    executable: str


class ProjectSetup(BaseModel):
    arguments: list
    start_time: datetime


class Project(ProjectBase):
    owner_id: int

    class Config:
        orm_mode = True
