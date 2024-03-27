#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session

from src.db.update import update_element


def project_update_parameters(db: Session, db_project, parameter: str, new_value: any):
    setattr(db_project, f'{parameter}', new_value)

    update_element(db, db_project)

    return {f'{parameter}': eval(f'db_project.{parameter}')}