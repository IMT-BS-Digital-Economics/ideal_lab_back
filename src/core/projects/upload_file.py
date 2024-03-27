#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 26/03/2024
    About: To upload file in project

"""
import os

import aiofiles

from src.core.settings import config

from src.core.utils.handle_system_execution import run_command


class InvalidFileExtension(Exception):
    """
    Throw an exception when an invalid file ext is found
    """


def verify_file_integrity(filename) -> None:
    """
    To verify the integrity of the file that will be uploaded
    :param filename:
    :return: Nothing in case of success
    :raise: InvalidFileExt if the file doesn't comply with the requirements
    """
    allowed_extensions = ('.csv', '.xlsx')

    if not filename.lower().endswith(allowed_extensions) or '.py' in filename.lower():
        raise InvalidFileExtension(f'{filename} is not a valid file')


async def upload_file(unique_id: str, file, dest: str):
    """
    Upload a file to a project in a desired location
    :param unique_id: unique id of the project
    :param file: file to be uploaded
    :param dest: destination of the file inside the project
    :return: Nothing in case of success
    """
    code_path = f"{config['PROJECT_DIR']}/{unique_id}/repository"

    if not os.path.isdir(code_path):
        raise ModuleNotFoundError(f"Project {unique_id} not found")

    if not os.path.isdir(f'{code_path}/{dest}'):
        raise ModuleNotFoundError(f"Destination {dest} not found")

    verify_file_integrity(file.filename)

    async with aiofiles.open(f'files/{file.filename}', 'wb+') as f:
        content = await file.read()
        await f.write(content)

    run_command(f'mv files/{file.filename} {code_path}/{dest}')
