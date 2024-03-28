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


class ProjectUpdate(ProjectBase):
    unique_id: Union[str, None] = None
    title: Union[str, None] = None
    description: Union[str, None] = None
    arguments: list = []
    executable: Union[str, None] = None
    status: Union[str, None] = None
    start_time: Union[datetime, None] = None
    auto_launch: Union[bool, None] = None


class ProjectSetup(BaseModel):
    arguments: list
    start_time: datetime


class ProjectCreateDirectory(BaseModel):
    path: str


class Project(ProjectBase):
    owner_id: int

    class Config:
        orm_mode = True
