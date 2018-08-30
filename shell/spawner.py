import multiprocessing


class Spawn:
    def __init__(self, bot, thread):
        self._bot = bot
        self._thread = thread

    @property
    def bot(self):
        return self._bot

    @property
    def thread(self):
        return self._thread


class Spawner:
    def __init__(self):
        self.spawns = []

    def spawn_bot(self, bot):
        if self.bot_loaded(bot.name):
            return

        def routine():
            bot.load_client()
            bot.start()

        thread = multiprocessing.Process(target=routine)
        spawned = Spawn(bot, thread)
        self.spawns.append(spawned)

    def start_bot(self, bot_name):
        if not self.bot_loaded(bot_name):
            return
        for spawn in self.spawns:
            if spawn.bot.name == bot_name:
                spawn.thread.start()

    def stop_bot(self, bot_name):
        if not self.bot_loaded(bot_name):
            return
        for spawn in self.spawns:
            if spawn.bot.name == bot_name:
                spawn.thread.terminate()

    def bot_loaded(self, bot_name):
        for spawn in self.spawns:
            if spawn.bot.name == bot_name:
                return True
        return False

    def bot_running(self, bot_name):
        if not self.bot_loaded(bot_name):
            return False
        for spawn in self.spawns:
            if spawn.bot.name == bot_name:
                return spawn.thread.is_alive()
