#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 07/07/2022
    About: 

"""

from os.path import isfile

from src.schemas import items
from src.core.settings import set_up_dir_name


def get_output(item: items.Item, output_name: str):
    fp: str = f'{set_up_dir_name(item)}/{output_name}.txt'

    if not isfile(fp):
        return None

    line = None

    with open(fp, 'r') as f:
        for line in f:
            pass

    if line:
        return {
            f'{output_name}': line
        }
