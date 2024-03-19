#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 18/03/2024
    About: To handle any functions to execute on the system code or command

"""

import subprocess

from traceback import format_exc

from src.core.utils.handle_logs import write_logs


class InvalidCommand(Exception):
    """
    Throw when an invalid command is executed
    """


def run_command(command, shell=False):
    """
    Run a command on the system
    :param command: the command to be runned
    :param shell: to extend command to the shell
    :return: the success output or raise an error message
    """

    if not shell:
        command = command.split(' ')

    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=shell)
    except FileNotFoundError as exc:
        write_logs(format_exc())
        raise InvalidCommand(f'File not found in command "{command}"')
    except subprocess.CalledProcessError as exc:
        write_logs(format_exc())
        raise InvalidCommand(f'Error running command "{command}"')

    if result.returncode != 0:
        write_logs(result.stderr)
        raise InvalidCommand(f'Error running command "{command}"')

    return result
