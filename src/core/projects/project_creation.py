#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 20/03/2024
    About: To create project

"""

from os import path

from src.core.settings import config

from src.core.utils.handle_system_execution import run_command


class InvalidNameError(Exception):
    """
    Throw when not valid name for directory is choosen
    """


def create_venv(folder_path: str, python_version: str) -> str:
    """
    Create a virtual env for the new repository
    :param folder_path: the path of the new repository
    :param python_version: version of python to use for setup env
    :return: venv path in success else raises an exception
    """

    venv_path = path.join(folder_path, '.venv')

    run_command(f'python{python_version} -m venv {venv_path}', shell=True)

    return venv_path


def install_python_dependencies(folder_path: str, venv_path: str) -> None:
    """
    Install all dependencies for the new repository
    :param folder_path: the path of the new repository
    :param venv_path:the path of the new repository
    :return:Nothing in case of success else raises an exception
    """

    venv_pip_path = venv_path + '/bin/pip3'

    requirements_path = path.join(folder_path, 'requirements.txt')

    if not path.isfile(venv_pip_path):
        raise FileNotFoundError(venv_pip_path)

    if not path.isfile(requirements_path):
        raise FileNotFoundError(requirements_path)

    run_command(f'{venv_pip_path} install -r {requirements_path}', shell=True)


def create_dir_in_project(directory_name: str, unique_id: str):
    """
    Create a directory inside the project code repository
    :param directory_name: the name to be created
    :param unique_id: unique id of the project
    :return: Nothing in case of success
    """

    code_path = f"{config['PROJECT_DIR']}/{unique_id}/repository"

    if not path.isdir(code_path):
        raise ModuleNotFoundError(f'The project name {unique_id} not found')

    run_command(f"mkdir -p {code_path}/{directory_name}")


def create_project_dir(repository: str, unique_id: str):
    """
    Create a project directory based on the repository to use
    :param repository: repository to be sued
    :param unique_id: unique id of the project
    :return: Nothing in case of success
    """

    code_path = f"{config['PROJECT_DIR']}/{unique_id}/repository"

    run_command(f"mkdir -p {code_path}")
    run_command(f"cp -r {config['SCRIPT_DIR']}/{repository}/* {code_path}",
                shell=True)

    venv_path = create_venv(code_path, "3.9")

    install_python_dependencies(code_path, venv_path)


