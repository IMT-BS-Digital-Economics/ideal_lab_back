import unittest

from os.path import isdir

from os import system

from src.core.utils.handle_env import get_env_variable
from src.core.projects.project_creation import create_project_dir
from src.core.projects.handle_project_environment import add_environment_variable, get_environment_variables, \
    update_environment_variable, del_environment_variable


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.unique_id = "6198397d-c881-49b4-91de-bcd96105177e"
        self.folder_path = f"{get_env_variable('PROJECT_DIR')}/{self.unique_id}"
        self.environment_var = [
            {'key': 'TEST', 'value': 'Hellooioooo'},
            {'key': 'TEST1', 'value': 'Allo?'},
            {'key': 'TEST2', 'value': 'Ciao?'}
        ]

        create_project_dir('Facebook_ad_delivery_estimate_24-19032024162808', self.unique_id)

    def tearDown(self):
        system(f'rm -rf {self.folder_path}')

    def test_a_create_project_dir(self):
        self.assertTrue(isdir(self.folder_path), True)

    def test_b_add_environment_variable(self):
        add_environment_variable(self.unique_id, self.environment_var[0])
        self.assertEqual(get_environment_variables(self.unique_id)[0], self.environment_var[0])

    def test_c_update_environment_variable(self):
        add_environment_variable(self.unique_id, self.environment_var[0])
        add_environment_variable(self.unique_id, self.environment_var[1])
        add_environment_variable(self.unique_id, self.environment_var[2])

        update_environment_variable(self.unique_id, {'key': 'TEST', 'value': 'Hey'})

        self.assertEqual(get_environment_variables(
            self.unique_id),
            [{'key': 'TEST', 'value': 'Hey'}] + self.environment_var[1:]
        )

    def test_e_delete_environment_variable(self):
        add_environment_variable(self.unique_id, self.environment_var[0])
        add_environment_variable(self.unique_id, self.environment_var[1])
        add_environment_variable(self.unique_id, self.environment_var[2])

        del_environment_variable(self.unique_id, self.environment_var[0])

        self.assertEqual(get_environment_variables(self.unique_id), self.environment_var[1:])


if __name__ == '__main__':
    unittest.main()
