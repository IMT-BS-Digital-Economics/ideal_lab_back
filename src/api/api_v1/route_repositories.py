#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 08/07/2022
    About: 

"""
import datetime
import os
import subprocess
from glob import glob
from os import listdir, path, system

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends

from src import schemas
from src.core.auth.auth_handler import verified_session
from src.core.auth.session_handler import verifier, cookie
from src.core.repositories.add_repository import add_repository
from src.core.utils.handle_system_execution import InvalidCommand, run_command
from src.db.database import get_db

from src.core.settings import config

router_repositories = APIRouter()


@router_repositories.get("/", dependencies=[Depends(cookie)])
async def get_repositories_available(session_data: schemas.SessionData = Depends(verifier),
                                     db: Session = Depends(get_db)):
    """
    Get all repositories from the project
    :param session_data:
    :param db:
    :return:
    """
    verified_session(db, session_data)

    if not path.isdir(config['SCRIPT_DIR']):
        os.system(f"mkdir {config['SCRIPT_DIR']}")

    return [{'title': element} for element in listdir(config['SCRIPT_DIR'])]


@router_repositories.get("/{project_name}", dependencies=[Depends(cookie)])
async def get_repositories_potential_executable(
        project_name: str,
        session_data: schemas.SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    dir_names: list = listdir(config['SCRIPT_DIR'])

    dir_path: str = None

    for dir_name in dir_names:
        if project_name in dir_name:
            dir_path = dir_name
            break

    if not dir_path:
        raise HTTPException(
            status_code=400,
            detail="Not able to retrieve this project..."
        )

    executables = glob(f'{config["SCRIPT_DIR"]}/{dir_path}/*.py')

    return [executable.split('/')[-1] for executable in executables]


@router_repositories.post("/clone", dependencies=[Depends(cookie)])
async def clone_repo(
        clone_data: schemas.repository_clone,
        session_data: schemas.SessionData = Depends(verifier),
        db: Session = Depends(get_db)):
    verified_session(db, session_data)

    try:
        message = add_repository(clone_data.user, clone_data.token, clone_data.repository, config['SCRIPT_DIR'], clone_data.version)
    except InvalidCommand as e:
        raise HTTPException(
            status_code=400,
            detail="Cloning operation failed due to invalid command error"
        )
    except FileNotFoundError as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Cloning operation failed due to unknown path"
        )

    return {'message': message}


@router_repositories.delete("/{repository_name}", dependencies=[Depends(cookie)])
async def delete_repository(
        repository_name: str,
        session_data: schemas.SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    repository_path = f"{config['SCRIPT_DIR']}/{repository_name}"

    if not path.isdir(repository_path):
        raise HTTPException(status_code=400, detail=f"Repository {repository_name} not found")

    run_command(f'rm -rf {repository_path}')

    return {'detail': f'Repository {repository_name} deleted'}
