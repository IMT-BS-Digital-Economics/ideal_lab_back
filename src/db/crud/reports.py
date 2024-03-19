#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session

from src.db import models

from src import schemas


def get_reports(db: Session, item_id: int) -> schemas.ReportBase:
    return db.query(models.Report).filter(models.Report.item_id == item_id).offset(0).limit(100).all()


def update_report(db: Session, db_report: models.Report):
    db.add(db_report)
    db.commit()
    db.refresh(db_report)


def create_report(db: Session, report: schemas.ReportBase, item_id: int):
    db_report = models.Report(**report.dict(), item_id=item_id)

    update_report(db, db_report)


