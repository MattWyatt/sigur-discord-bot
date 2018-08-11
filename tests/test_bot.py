import unittest
import os
import json
from components import exceptions
from components import bot
from components import subroutine


@subroutine.add_subroutine({
    "name": "subroutine1",
    "description": "test subroutine",
    "author": "Saviour#8988"
})
class Subroutine1(subroutine.Subroutine):
    pass


def make_test_config(config):
    file_path = "test_config.json"
    with open(file_path, "w+") as file:
        file.write(json.dumps(config))
        if not config:
            file.write("bad config")
        file.close()
    return file_path


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = bot.Bot("SigurTest")
        self.test_config1 = {"value1": True, "value2": False}
        self.test_config2 = {"value1": False, "value2": True}

    def tearDown(self):
        os.remove(make_test_config({}))

    # test loading a dictionary as a config
    def test_load_config_dict(self):
        self.bot.load_config(self.test_config1)
        self.assertTrue(self.bot.config["value1"])
        self.assertFalse(self.bot.config["value2"])

    # test loading a file as a config
    def test_load_config_file(self):
        config_file = make_test_config(self.test_config2)
        self.bot.load_config(config_file)
        self.assertFalse(self.bot.config["value1"])
        self.assertTrue(self.bot.config["value2"])

    def test_config_errors(self):
        try:
            self.bot.load_config("not a valid path")
        except FileNotFoundError:
            # if we get an InvalidConfiguration error, it works
            self.assertTrue(True)
            return
        # and if not, it didn't work
        self.assertTrue(False)

        config_file = make_test_config(None)
        try:
            self.bot.load_config(config_file)
        except exceptions.InvalidConfiguration:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_load_subroutine(self):
        self.assertFalse(self.bot.subroutine_loaded("subroutine1"))
        self.bot.load_subroutine("subroutine1")
        self.assertTrue(self.bot.subroutine_loaded("subroutine1"))
        self.bot.unload_subroutine("subroutine1")

    def test_unload_subroutine(self):
        self.bot.load_subroutine("subroutine1")
        self.assertTrue(self.bot.subroutine_loaded("subroutine1"))
        self.bot.unload_subroutine("subroutine1")
        self.assertFalse(self.bot.subroutine_loaded("subroutine1"))


