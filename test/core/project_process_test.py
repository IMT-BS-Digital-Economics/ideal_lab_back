from datetime import datetime

import unittest

from os.path import isdir

from os import system

from time import sleep

from src.core.projects.handle_process import load_project_process, ProcessError
from src.core.projects.project_creation import create_project_dir
from src.core.utils.handle_env import get_env_variable


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.unique_id = '3ffd54db-472f-4ee8-a7cf-c2a2ff50ec4e'

        if not isdir(f'{get_env_variable("PROJECT_DIR")}/{self.unique_id}'):
            create_project_dir('Facebook_ad_delivery_estimate_24-19032024162808', self.unique_id)

    def test_a_start_process(self):
        project_process = load_project_process(self.unique_id)

        self.assertEqual(
            project_process.start_process('50states_collect.py', ["Test"]).value,
            "Operational"
        )

        sleep(10)

    def test_c_stop_test_process(self):
        project_process = load_project_process(self.unique_id)

        self.assertEqual(
            project_process.stop_process().value,
            "Manually stopped"
        )

        sleep(10)

    def test_d_restart(self):
        project_process = load_project_process(self.unique_id)

        self.assertEqual(
            project_process.restart_process().value,
            "Operational"
        )

        sleep(5)

    def test_d_turn_off_process(self):
        project_process = load_project_process(self.unique_id)

        self.assertEqual(
            project_process.turn_off_process().value,
            "Powered Off"
        )




if __name__ == '__main__':
    unittest.main()
