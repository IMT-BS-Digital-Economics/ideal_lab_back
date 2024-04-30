#!/usr/bin/env python3

"""
        ideal_lab_back

    Author: bricetoffolon
    Created on: 19/03/2024
    About: To handle project statuses

"""
from datetime import datetime
from os import kill, path
from time import sleep

from signal import SIGSTOP, SIGCONT, SIGTERM

from subprocess import Popen

from psutil import Process, NoSuchProcess

from enum import Enum

from src.core.settings import config

from src.core.utils.handle_system_execution import run_command


def send_signal(process_id: int, signal: int):
    """
    Send signal to a desired process
    :param process_id: process id of the process to kill
    :param signal: signal to send to the process
    :return: nothing in case of success
    """

    if process_id != -1:
        kill(process_id, signal)


class ProcessError(Exception):
    """Throw when a process is occuring an error"""


class Status(Enum):
    off = "Powered Off"
    running = "Operational"
    stopped = "Manually stopped"
    fail = "Failure Detected"
    zombie = "Zombie Detected"
    creating = "Creating project"
    ready = "Ready to launch"

    @staticmethod
    def from_string(status_string: str):
        """
        Get status from a psutil.status() to retrieve the variable from Enum
        :param status_string: status
        :return: the Status from the class
        :raise ValueError: if not valid status
        """

        for status in Status:
            if status.name == status_string:
                return status
        raise ValueError(f"Invalid status: {status_string}")


class ProjectProcess:
    """
    Process of project
    """

    def __init__(self, unique_id: str, process_id: int = -1):
        """
        Init the Status class
        :param unique_id: unique_id of the project
        """

        self.unique_id = unique_id
        self.process_id = process_id
        self.folder_path = f"{config.get('PROJECT_DIR')}/{unique_id}"
        self.code_path = f"{config.get('PROJECT_DIR')}/{unique_id}/repository"
        self.log_path = f'{self.folder_path}/logs/output'

    def restart_process(self):
        """
        Restart the process
        :return: Nothing
        """

        current_status = self.get_process_status()

        if current_status != Status.stopped:
            raise ProcessError(f'Something went wrong cannot restart: {current_status.value}')

        return Status.from_string('running')

    def start_process(self, executable: str, arguments: list):
        """
        Start the process
        :param executable: execution file to start the process
        :param arguments: arguments to add to start the project
        :return: Process status
        """

        python_path = f"./.venv/bin/python"

        cmd = f'{python_path} -u {executable} {" ".join(arguments)}'

        current_status = self.get_process_status()

        if current_status != Status.off:
            raise ProcessError(f'Something went wrong cannot start: {current_status.value}')

        start_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

        with (
            open(f'{self.log_path}_{start_time}.txt', 'wb') as out,
            open(f'{self.folder_path}/pid', 'w') as pid_file
        ):
            process = Popen(cmd, stdout=out, stderr=out, cwd=self.code_path, shell=True)

            self.process_id = process.pid
            pid_file.write(str(self.process_id))

        return Status.from_string('running')

    def stop_process(self):
        """
        Stop process
        :return: status
        """
        current_status = self.get_process_status()

        if current_status != Status.running:
            raise ProcessError(f'Something went wrong cannot stop: {current_status.value}')

        send_signal(self.process_id, SIGSTOP)

        return Status.from_string('stopped')

    def turn_off_process(self, failed=False, zombie=False):
        """
        Turn off process
        failed: if process have failed
        zombie: if process is in zombie stat
        :return: status
        """

        print(f'In when crash {self.process_id}')

        if not failed:
            send_signal(self.process_id, SIGTERM)

        self.process_id = -1

        print(zombie)

        if not zombie:
            pid_path = f'{self.folder_path}/pid'

            if path.isfile(pid_path):
                run_command(f'rm -rf {pid_path}', shell=True)

        return Status.from_string('off')

    def get_process_status(self) -> Status:
        """
        Determine process status from the
        :return: process status
        """
        try:
            process = Process(self.process_id)
            current_status = process.status()
        except (NoSuchProcess, ValueError):
            if not path.isfile(f'{self.folder_path}/pid'):
                return Status.off
            else:
                self.turn_off_process(failed=True)
                return Status.fail

        if current_status == "zombie":
            self.turn_off_process(zombie=True)

        return Status.from_string(current_status)


def load_project_process(unique_id: str) -> ProjectProcess:
    """
    Load project process based only on the unique_id
    :param unique_id:
    :return: A class object ProjectProcess
    """
    pid_path = f'{config.get("PROJECT_DIR")}/{unique_id}/pid'

    pid = -1

    if path.isfile(pid_path):
        with open(pid_path, 'r') as f:
            pid = int(f.read())

    return ProjectProcess(unique_id, pid)
