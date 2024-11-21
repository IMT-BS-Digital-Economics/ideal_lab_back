#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.db.models import Project
from src.db.models import User

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def get_project_by_title(db: Session, title: str, owner_id: int) -> Project:
    return db.query(Project).filter(Project.title == title, Project.owner_id == owner_id).first()


def get_project_by_unique_id(db: Session, unique_id: str, owner_id: int) -> Project:
    try:
        return db.query(Project).filter(Project.unique_id == unique_id, Project.owner_id == owner_id).first()
    except NoResultFound:
        return None
    

def get_user_projects(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(Project).filter(Project.owner_id == owner_id).limit(limit).all()