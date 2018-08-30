import unittest
import time
from components import bot
from components import database
from shell import spawner
from augments import *


class TestSpawner(unittest.TestCase):
    def setUp(self):
        self.bot = bot.Bot("SigurTest")
        self.bot.load_database(database.Database(in_memory=True))
        self.bot.load_config("tests/testconfig.json")
        self.spawner = spawner.Spawner()

    def test_spawn_bot(self):
        self.spawner.spawn_bot(self.bot)
        self.assertEqual(self.spawner.spawns[0].bot, self.bot)

    def test_start_stop(self):
        self.spawner.spawn_bot(self.bot)
        self.spawner.start_bot(self.bot.name)
        # wait roughly 5 seconds for the bot to start
        time.sleep(5)
        self.assertTrue(self.spawner.bot_running(self.bot.name))
        self.spawner.stop_bot(self.bot.name)
        time.sleep(5)
        self.assertFalse(self.spawner.bot_running(self.bot.name))

    def test_bot_loaded(self):
        self.spawner.spawn_bot(self.bot)
        self.assertTrue(self.spawner.spawn_bot)
