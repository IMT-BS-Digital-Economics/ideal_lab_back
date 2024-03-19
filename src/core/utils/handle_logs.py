#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 19/03/2024
    About: To handle logs

"""

from os import path

from datetime import datetime


def write_logs(content: str) -> None:
    time = datetime.now().strftime('%d%m%Y')

    if not path.isdir('logs'):
        return None

    with open(f'logs/{time}.txt', 'a') as f:
        f.write(f'{time}: {content}\n------\n')
