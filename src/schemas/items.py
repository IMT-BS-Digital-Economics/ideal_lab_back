#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
    path: str
    arguments: list = []
    time_to_start: str


class ItemCreate(ItemBase):
    pass


class ItemProcess(ItemBase):
    process_id: Union[int, None] = None


class ItemUpdate(ItemBase):
    title: Union[str, None] = None
    description: Union[str, None] = None
    path: Union[str, None] = None
    arguments: list = []
    time_to_start: Union[str, None] = None

class ItemUploadFile(ItemBase):
    path: Union[str, None] = None

class DownloadFile(BaseModel):
    path: Union[str, None] = None
    filename: Union[str, None] = None


class Item(ItemBase):
    start_time: Union[str, None] = None
    item_status: Union[str, None] = None
    id: int
    owner_id: int

    class Config:
        orm_mode = True
