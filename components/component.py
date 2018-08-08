import logging


class Component:
    def __init__(self, inherit=None):
        self._name = None
        self._bot = None
        self._client = None
        self._database = None
        self._logger = None
        self._config = None

        if inherit:
            self._name = inherit.name
            self._bot = inherit.bot
            self.set_client(inherit.client)
            self.set_database(inherit.database)
            self._logger = inherit.logger
            self.set_config(inherit.config)

    def set_name(self, name):
        self._name = name

    def set_client(self, client):
        self._client = client

    def set_database(self, database):
        self._database = database

    def set_logger(self, logger_name):
        self._logger = logging.getLogger(logger_name)

    def set_config(self, config):
        self._config = config

    @property
    def name(self):
        return self._name

    @property
    def bot(self):
        return self._bot

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self._database

    @property
    def logger(self):
        return self._logger

    @property
    def config(self):
        return self._config
