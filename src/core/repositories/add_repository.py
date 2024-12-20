#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 18/03/2024
    About: To handle any function to add a new repository

"""
from datetime import datetime

from src.core.utils.handle_system_execution import run_command


def clone_repository(username: str, token: str, repository_name: str):
    """
    Clone a repository and add it to the repositories folder
    :param username: username of the git user
    :param token: token of the git user
    :param repository_name: name of the repository that needs to be cloned
    :return: Nothing in case of success otherwise raises an exception
    """

    run_command(f'git clone https://{username}:{token}@github.com/{repository_name}.git')


def save_repository_in_dir(dest_path: str, repository_name: str) -> str:
    """
    Save the repository to the directory
    :param dest_path: path of the directory where the repository will be saved
    :param repository_name: name of the repository that needs to be saved
    :return: a str, New saved repository in case of success otherwise raises exception
    """

    if '/' in repository_name and not repository_name.endswith('/'):
        repository_name = repository_name.split('/')[1]

    folder_path = f'{dest_path}/{repository_name}-{datetime.now().strftime("%d%m%Y%H%M%S")}'

    run_command(f'mkdir -p {folder_path}')
    run_command(f'mv {repository_name}/* {folder_path}/', shell=True)
    run_command(f'rm -rf {repository_name}')

    return folder_path


def add_repository(username: str, token: str, repository_name: str, dest: str, python_version: str) -> str:
    """
    Add a new repository to the repositories folder
     :param username: username of the git user
    :param token: token of the git user
    :param repository_name: name of the repository that needs to be cloned
    :param dest: path of the directory where the repository will be saved
    :param python_version: version of python to use for setup env
    :return: A success message or error message
    """

    clone_repository(username, token, repository_name)

    folder_path = save_repository_in_dir(dest, repository_name)

    repository_name = folder_path.split('/')[-1]

    return f'Successfully created the repository: {repository_name}'
