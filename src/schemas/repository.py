#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 13/12/2023
    About: 

"""
from typing import Optional

from pydantic import BaseModel

class repository_clone(BaseModel):
    user: str
    token: str
    repository: str
    version: str

class repository_user(BaseModel):
    user: str
    token: str
