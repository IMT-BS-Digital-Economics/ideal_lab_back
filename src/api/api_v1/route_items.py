#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""
import os.path

import aiofiles

from fastapi import APIRouter, HTTPException, Depends, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from os import system

from src import schemas
from src.core.items.edit.edit_handler import edit_parameter, check_parameter
from src.core.items.edit.parameter_enum import Parameter
from src.core.items.output import get_output
from src.core.items.status.status_handler import check_status, action
from src.core.items.status.status_enum import Status
from src.core.settings import config
from src.db import crud
from src.core.auth.auth_handler import verified_session
from src.db.database import get_db
from src.core.auth.session_handler import verifier, cookie
from src.core.items.watching_task import watching_item_run

router_items = APIRouter()


@router_items.get("/list", dependencies=[Depends(cookie)])
async def get_items_list(session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    user = verified_session(db, session_data)

    return {"list": user.items}


@router_items.get("/status", dependencies=[Depends(cookie)])
def get_status(session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    verified_session(db, session_data)

    return [e.value for e in Status]


@router_items.get("/parameters", dependencies=[Depends(cookie)])
def get_parameters(session_data: schemas.SessionData = Depends(verifier),
              db: Session = Depends(get_db)):
    verified_session(db, session_data)

    return [e for e in Parameter]


@router_items.get("/{item_id}", dependencies=[Depends(cookie)], response_model=schemas.Item)
async def get_item(item_id, session_data: schemas.SessionData = Depends(verifier), db: Session = Depends(get_db)):
    db_user: schemas.User = verified_session(db, session_data)

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if item:
        return item
    else:
        raise HTTPException(
            status_code=400,
            detail="Item not found"
        )


@router_items.post("/add", dependencies=[Depends(cookie)])
async def add_item(item: schemas.ItemCreate, session_data: schemas.SessionData = Depends(verifier),
                   db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    if crud.get_items_by_title(db, item.title, db_user.id):
        raise HTTPException(
            status_code=400,
            detail="Item already exist"
        )

    crud.create_user_item(db, item, user_id=db_user.id)

    return {"detail": f"A new item named {item.title} has been created !"}


@router_items.delete("/{item_id}", dependencies=[Depends(cookie)])
async def del_item(item_id: str, session_data: schemas.SessionData = Depends(verifier),
                   db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    return crud.del_items(db, item_id, db_user.id)


@router_items.post("/{item_id}/status/{item_status}", dependencies=[Depends(cookie)])
async def update_status(item_id: str, item_status: str, background_task: BackgroundTasks,session_data: schemas.SessionData = Depends(verifier),
                        db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if item:
        if not check_status(item_status):
            raise HTTPException(
                status_code=400,
                detail="Status not exist"
            )

        if item_status == "running":
            background_task.add_task(watching_item_run, db, item.title, item.owner_id)

        result: str = action(db, db_user, item, item_status)

        if 'yet' in result:
            raise HTTPException(
                status_code=400,
                detail=result
            )

        crud.update_item_status(db, item.title, item_status, db_user.id)

        return result

    else:
        raise HTTPException(
            status_code=400,
            detail="Item not found"
        )


@router_items.get("/{item_id}/output", dependencies=[Depends(cookie)])
def get_item_output(item_id: str, session_data: schemas.SessionData = Depends(verifier),
                    db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if item:
        result = get_output(item, 'out')

        if not result:
            raise HTTPException(
                status_code=400,
                detail="Item hasn't output history yet"
            )

        return result

    else:
        raise HTTPException(
            status_code=400,
            detail="Item not found"
        )


@router_items.get("/{item_id}/err_output", dependencies=[Depends(cookie)])
def get_item_output(item_id: str, session_data: schemas.SessionData = Depends(verifier),
                    db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if item:
        result = crud.get_reports(db, item.id)

        if not result:
            raise HTTPException(
                status_code=400,
                detail="Item hasn't output history yet"
            )

        return result

    else:
        raise HTTPException(
            status_code=400,
            detail="Item not found"
        )


@router_items.post("/{item_id}/edit/{parameter}", dependencies=[Depends(cookie)])
def edit_item(item_new: schemas.ItemUpdate, item_id: str, parameter: str, session_data: schemas.SessionData = Depends(verifier),
              db: Session = Depends(get_db)):
    db_user = verified_session(db, session_data)

    check_parameter(parameter)

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if item:
        if eval(f'item_new.{parameter}') is None:
            raise HTTPException(
                status_code=400,
                detail=f"Parameter key is different from {parameter}"
            )

        return edit_parameter(db, item, parameter, eval(f'item_new.{parameter}'))

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Item not found with id: {item_id}"
        )


@router_items.post("/{item_id}/uploadfile/{path_info}", dependencies=[Depends(cookie)])
async def upload_file(
        item_id: str,
        file: UploadFile,
        path_info: str,
        session_data: schemas.SessionData = Depends(verifier),
        db: Session = Depends(get_db)
):
    db_user = verified_session(db, session_data)

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file have been provided"
        )

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if not item:
        raise HTTPException(
            status_code=400,
            detail="No item found"
        )

    async with aiofiles.open(f'files/{file.filename}', 'wb+') as f:
        content = await file.read()
        await f.write(content)

    print(item.path[:item.path.rfind("/")])

    system(f'mv files/{file.filename} {config["SCRIPT_DIR"]}/{item.path[:item.path.rfind("/")]}/{path_info}')

    return {'filename': file.filename}

@router_items.get("/{item_id}/download_file", dependencies=[Depends(cookie)])
async def download_file (
        item_id: str,
        path_info: schemas.items.DownloadFile,
        session_data: schemas.SessionData = Depends(verifier),
        db: Session = Depends(get_db)
    ):
    db_user = verified_session(db, session_data)

    item = crud.get_items_by_id(db, item_id, db_user.id)

    if not item:
        raise HTTPException(
            status_code=400,
            detail="No item found"
        )

    dir_path = f'{config["SCRIPT_DIR"]}/{item.path[:item.path.rfind("/")]}'

    path_info.path = f'{dir_path}{path_info.path}'

    if os.path.isdir(f'{path_info.path}') and os.path.isfile(f'{path_info.path}/{path_info.filename}'):
        return FileResponse(f'{path_info.path}/{path_info.filename}', media_type="application/octet-stream", filename=path_info.filename)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid path: {path_info.path}/{path_info.filename}"
        )




