import os
import shutil
import subprocess
import unittest
from os.path import normpath as norm

PATH = 'test/data/generated/'
IMPORTED_GRAPH_NAME = 'test-vault'
IMPORTED_VAULT = os.path.join('test/data/test/', IMPORTED_GRAPH_NAME)


class MigratorE2E_TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.delete_log_file()
        module_directory = os.path.dirname(__file__)
        # we're in test/prioritise/e2e, so go up two levels to test,
        # then down to data/generated
        working_directory = norm(os.path.join(module_directory,
                                              '../../data/generated'))
        if os.path.exists(working_directory):
            shutil.rmtree(working_directory)
        shutil.copytree(IMPORTED_VAULT, working_directory)
        # normalize file locations for Windows
        code_location = norm('../../../src/logseq/migration/migrater.py')
        self.result = subprocess.run(
            ['python3',
             code_location,
             '.',
             ],
            cwd=working_directory
        )

    def test_app_runs(self):
        self.assertEqual(0, self.result.returncode)

    def test_app_creates_log_file(self):
        self.assertTrue(os.path.exists(PATH))


    def delete_log_file(self):
        log_path = os.path.join(PATH, 'migration.log')
        if os.path.exists(log_path):
            os.remove(log_path)




if __name__ == '__main__':
    unittest.main()
