#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from typing import Union

from pydantic import BaseModel


class ReportBase(BaseModel):
    time: Union[str, None] = None
    traceback: Union[str, None] = None

    class Config:
        orm_mode = True