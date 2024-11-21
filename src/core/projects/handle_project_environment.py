#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 21/03/2024
    About: To handle project environment

"""

from os.path import isfile

from typing import TypedDict, List

from src.core.settings import config

class EnvVar(TypedDict):
    key: str
    value: str


def add_environment_variable(unique_id: str, env_var: EnvVar):
    """
    Add an environment variable to the project's environment.
    :param unique_id: unique id of the project
    :param env_var: environment variable to be added to the environment
    :return: nothing in case of success
    """

    env_path = f"{config['PROJECT_DIR']}/{unique_id}/repository/.env"

    variable = f'{env_var["key"]}={env_var.get("value")}'

    with open(env_path, 'a') as f:
        f.write(f'{variable}\n')


def get_environment_variables(unique_id: str) -> List[EnvVar]:
    """
    Get environment_variables from the project's
    :param unique_id: unique id of the project
    :return: list of environment variables
    :raise: FileNotFoundError if environment variable not found
    """

    env_path = f"{config['PROJECT_DIR']}/{unique_id}/repository/.env"

    if not isfile(env_path):
        raise FileNotFoundError('Environment file not found for project ' + unique_id)

    with open(env_path, 'r') as f:
        variables = f.readlines()
        parsed_variables = [{
            'key': variable.split('=')[0],
            'value': variable.split('=')[1].replace('\n', '')
        } for variable in variables if '=' in variable]

        return parsed_variables


def update_environment_file(env_path: str, old_value: str, new_value: str):
    """
    To update the environment file
    :param env_path: path to the environment file
    :param old_value: old value to be replaced
    :param new_value: new value to replace with
    :return: Nothing
    """

    with open(env_path, 'r') as f:
        content = f.read()

    with open(env_path, 'w') as f:
        f.write(content.replace(old_value, new_value))


def update_environment_variable(unique_id: str, env_var: EnvVar):
    """
    To update the variable value, we need to delete it from the file in first place to replace it
    :param unique_id: unique id of the project
    :param env_var: environment variable to be added to the environment
    :return: nothing in case of success
    """

    env_path = f"{config['PROJECT_DIR']}/{unique_id}/repository/.env"

    new_variable = f'{env_var["key"]}={env_var.get("value")}'

    with open(env_path, 'r') as f:
        env_variables = [variable for variable in f.readlines() if env_var["key"] == variable.split('=')[0]]

    if not env_variables:
        raise ValueError(f"Environment variable {env_var['key']} not found")

    update_environment_file(env_path, env_variables[0], new_variable + '\n')


def del_environment_variable(unique_id: str, env_var: EnvVar) -> str:
    """
    To delete the variable value
    :param unique_id: unique id of the project
    :param env_var: environment variable to be added to the environment
    :return: name of deleted variable
    """

    env_path = f"{config['PROJECT_DIR']}/{unique_id}/repository/.env"

    variable = f'{env_var["key"]}={env_var.get("value")}'

    update_environment_file(env_path, variable, '')

    return env_var['key']
