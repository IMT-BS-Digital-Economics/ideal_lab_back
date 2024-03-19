#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session


def update_element(db: Session, element):
    db.add(element)
    db.commit()
    db.refresh(element)