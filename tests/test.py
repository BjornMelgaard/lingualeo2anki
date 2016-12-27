from os import path, system
from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, call

from server.config import config
from .testdata import testdata_without_parent, testdata_with_parent

test_dir_path     = path.dirname(__file__)
root_dir_path     = path.dirname(test_dir_path)
debug_path        = path.join(test_dir_path, "debug.log")
start_server_path = path.join(root_dir_path, 'start_server.sh')

# recreate debug.log
open(debug_path, 'w').close()


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))


class TestHandler(TestCase):

    def setUp(self):
        cmd = [
            start_server_path,
            '-f', path.join(test_dir_path, 'anki.csv'),
            '--debug'
        ]
        self.debug_file = open(debug_path, 'a')
        self.server = Popen(cmd, shell=True, universal_newlines=True,
                            stdout=self.debug_file, stderr=STDOUT)

    def tearDown(self):
        try:
            self.server.communicate(timeout=2)
        except TimeoutExpired:
            self.server.kill()
            system("lsof -i :3100 | awk '{ print $2 }' | tail -n +2 | xargs kill")
        finally:
            self.debug_file.close()

    def testWordWithoutParent(self):
        print("")
        # pass
