#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 06/07/2022
    About: 

"""

from enum import Enum


class Status(Enum):
    off = "off"
    running = "running"
    paused = "paused"
    unreachable = "unreachable"