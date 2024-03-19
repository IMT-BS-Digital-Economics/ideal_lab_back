#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from dotenv import dotenv_values
from os.path import isdir
from os import system, environ

config = dotenv_values('.env') if dotenv_values('.env') else environ


def set_up_dir_name(db_item, create=True) -> str:
    dir_name: str = f'items/{db_item.title.replace(" ", "_")}_owner_id{db_item.owner_id}'

    if not isdir(dir_name) and create:
        system(f'mkdir {dir_name}')
    return dir_name
