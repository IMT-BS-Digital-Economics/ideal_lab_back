#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 20/03/2024
    About: To handle projects related route

"""

from traceback import format_exc

from os import listdir
from os.path import isfile

from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, UploadFile, BackgroundTasks, Form

from sqlalchemy.orm import Session

from src.core.auth.auth_handler import verified_session
from src.core.projects.handle_process import load_project_process, ProcessError
from src.core.projects.handle_project_environment import EnvVar, add_environment_variable, update_environment_variable, \
    del_environment_variable, get_environment_variables
from src.core.projects.project_creation import create_project_dir, create_dir_in_project
from src.core.projects.update import check_parameter, edit_parameter
from src.core.projects.upload_file import upload_file
from src.core.projects.worker import monitoring_time_worker
from src.schemas import SessionData, Project
from src.schemas.projects import ProjectCreate, ProjectSetup, ProjectCreateDirectory, ProjectUpdate
from src.core.auth.session_handler import verifier, cookie
from src.db.database import get_db
from src.db import crud

router_project = APIRouter()


@router_project.post('/', dependencies=[Depends(cookie)])
async def create_project(
        project: ProjectCreate,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    unique_id = str(uuid4())

    crud.create_user_project(db, project, user.id, unique_id)

    create_project_dir(project.repository, unique_id)

    return crud.get_project_by_unique_id(db, unique_id, user.id)


@router_project.delete('/{unique_id}', dependencies=[Depends(cookie)])
async def delete_project(
        unique_id: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    return crud.del_project(db, unique_id, user.id)


@router_project.get('/{unique_id}', dependencies=[Depends(cookie)])
async def get_project(
        unique_id: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    return crud.get_project_by_unique_id(db, unique_id, user.id)


@router_project.get('/', dependencies=[Depends(cookie)])
async def get_projects(
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    return {'details': crud.get_projects(db)}


@router_project.post('/{unique_id}/setup', dependencies=[Depends(cookie)])
async def setup_project(
        unique_id: str,
        project_setup: ProjectSetup,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    project = crud.get_project_by_unique_id(db, unique_id, user.id)

    crud.project_update_parameters(db, project, 'arguments', project_setup.arguments)
    crud.project_update_parameters(db, project, 'start_time', project_setup.start_time)

    return crud.get_project_by_unique_id(db, unique_id, user.id)


@router_project.post('/{unique_id}/env/', dependencies=[Depends(cookie)])
async def add_env_var_to_project(
        unique_id: str,
        environment_variable: EnvVar,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    add_environment_variable(unique_id, environment_variable)

    return {'detail': f'Environment variable uploaded'}


@router_project.get('/{unique_id}/env/', dependencies=[Depends(cookie)])
async def get_env_vars(
        unique_id: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    return {f'data: {get_environment_variables(unique_id)}'}


@router_project.post('/{unique_id}/env/update', dependencies=[Depends(cookie)])
async def update_env_var_to_project(
        unique_id: str,
        environment_variable: EnvVar,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    update_environment_variable(unique_id, environment_variable)


@router_project.delete('/{unique_id}/env/', dependencies=[Depends(cookie)])
async def delete_env_var(
        unique_id: str,
        environment_variable: EnvVar,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)
    
    return {f'message: we deleted this variable: {del_environment_variable(unique_id, environment_variable)}'}


@router_project.post('/{unique_id}/status/{status}', dependencies=[Depends(cookie)])
async def update_status(
        unique_id: str,
        status: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    project_process = load_project_process(unique_id)

    try:
        if status == 'off':
            status = project_process.turn_off_process()
        if status == 'running':
            project = crud.get_project_by_unique_id(db, unique_id, user.id)
            status = project_process.start_process(project.executable, project.arguments)
        if status == 'stopped':
            status = project_process.stop_process()
        if status == 'restart':
            status = project_process.restart_process()
    except ProcessError as exc:
        return {'error': str(exc)}

    return {'message': status.value}


@router_project.get('/{unique_id}/status', dependencies=[Depends(cookie)])
async def get_status(
        unique_id: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    project_process = load_project_process(unique_id)

    return {'status': project_process.get_process_status()}


@router_project.post('/{unique_id}/trigger/auto_launch', dependencies=[Depends(cookie)])
async def launch_worker(
        unique_id: str,
        background_task: BackgroundTasks,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    user = verified_session(db, session_data)

    project = crud.get_project_by_unique_id(db, unique_id, user.id)

    if project.auto_launch:
        crud.project_update_parameters(db, project, 'auto_launch', False)
    else:
        crud.project_update_parameters(db, project, 'auto_launch', True)
        background_task.add_task(monitoring_time_worker, unique_id, user.id, db)

    db.refresh(project)

    return project


@router_project.post('/{unique_id}/directory', dependencies=[Depends(cookie)])
async def create_directory(
        unique_id: str,
        directory_information: ProjectCreateDirectory,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    create_dir_in_project(directory_information.path, unique_id)

    return {'message': f'Directory {directory_information.path} created successfully'}


@router_project.post("/{unique_id}/upload/", dependencies=[Depends(cookie)])
async def upload(
        unique_id: str,
        file: UploadFile = Form(...),
        path: str = Form(...),
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    await upload_file(unique_id, file, path)

    return {'message': f'Your file has been uploaded'}


@router_project.get("/{unique_id}/logs", dependencies=[Depends(cookie)])
async def get_logs_files(
        unique_id: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    project_process = load_project_process(unique_id)

    return [file.replace('.txt', '') for file in listdir(f'{project_process.folder_path}/logs') if isfile(f'{project_process.folder_path}/logs/{file}')]


@router_project.get("/{unique_id}/log/{log_file}", dependencies=[Depends(cookie)])
async def get_logs(
        unique_id: str,
        log_file: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    verified_session(db, session_data)

    project_process = load_project_process(unique_id)

    with open(f'{project_process.folder_path}/logs/{log_file}.txt', "r") as file:
        content = file.readlines()

    return {'details': content}


@router_project.post("/{unique_id}/update/{parameter}", dependencies=[Depends(cookie)])
def update_project(
        updated_project: ProjectUpdate,
        unique_id: str,
        parameter: str,
        session_data: SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    db_user = verified_session(db, session_data)

    check_parameter(parameter)

    project = crud.get_project_by_unique_id(db, unique_id, db_user.id)

    if project:
        if eval(f'updated_project.{parameter}') is None:
            raise HTTPException(
                status_code=400,
                detail=f"Parameter key is different from {parameter}"
            )

        return edit_parameter(db, project, parameter, eval(f'updated_project.{parameter}'))

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Item not found with id: {unique_id}"
        )








