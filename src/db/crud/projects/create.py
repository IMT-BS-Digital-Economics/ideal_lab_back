#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session

from src.schemas.projects import ProjectCreate, Project

from src.db import models

from src.db.update import update_element

from src.core.projects.handle_process import Status


def create_user_project(db: Session, project: ProjectCreate, user_id: int, unique_id: str) -> Project:
    """
    Creates a new project in the database associated with a specific user.
    db (Session): The SQLAlchemy database session used to execute database operations. This session facilitates transactions and interactions with the database.
    project (ProjectCreate): An instance of ProjectCreate, which is a Pydantic model or a similar structure that contains the information needed to create a new project. This typically includes details like the project's title, description, and any other required attributes that are not auto-generated.
    user_id (int): The unique identifier (ID) of the user who owns the project. This ID is used to associate the new project with a user in the database.
    returns: An instance of the Project model representing the newly created project in the database. This object includes all the properties of the project, including its unique ID, title, description, status, and the user it's associated with.
    unique_id (str): The unique id of the collect
    """
    db_project = models.Project(
        unique_id=unique_id,
        title=project.title,
        description=project.description,
        status=Status.creating.value,
        repository=project.repository,
        executable=project.executable,
        owner_id=user_id
    )

    update_element(db, db_project)

    return db_project
