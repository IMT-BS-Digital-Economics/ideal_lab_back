#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.db.models import Project


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def get_project_by_title(db: Session, title: str, owner_id: int) -> Project:
    return db.query(Project).filter(Project.title == title, Project.owner_id == owner_id).first()


def get_project_by_unique_id(db: Session, unique_id: str, owner_id: int) -> Project:
    try:
        return db.query(Project).filter(Project.unique_id == unique_id, Project.owner_id == owner_id).first()
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Project not found")