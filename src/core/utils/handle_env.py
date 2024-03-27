#!/usr/bin/env python3

"""
        AWSBedrock-model-interactive-prompt-test

    Author: bricetoffolon
    Created on: 20/02/2024
    About: To handle environnement variable

"""

from os import getenv

from dotenv import dotenv_values


class MissingEnvironmentVariableError(Exception):
    """Throw when environment variable is missing"""


class MissingEnvFileError(Exception):
    """Throw when environment file is missing"""


def get_env():
    env: dict = dotenv_values('.env')

    if not env:
        raise MissingEnvFileError("No .env file found in repository")

    return env


def get_env_variable(env_var_name):
    """
    Get environement variable
    :param env_var_name: name of the variable you want
    :return: variable value or None
    """
    try:
        config = get_env()
        env_value = config.get(env_var_name)
    except MissingEnvFileError:
        env_value = getenv(env_var_name)

    if not env_value:
        raise MissingEnvironmentVariableError(f"Environment variable {env_var_name} is missing")

    return env_value
