import os
import json
import logging
import discord
import asyncio
from components import exceptions
from components import component
from components import subroutine
from components import database


class Bot(component.Component):
    def __init__(self, name, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.basicConfig(level=logging.INFO)

        self.set_name(name)
        self.set_logger(self.name)
        self.logger.setLevel(logging.DEBUG)

        # array of subroutine objects
        self.subroutines = []

        if config:
            self.load_config(config)

        self._bot = self

    def load_event_handlers(self):
        if not self.client:
            self.logger.error("attempted to load event handlers without client")
            raise exceptions.ClientNotLoaded

        # event handlers
        @self.client.event
        async def on_ready():
            self.logger.info("bot started with id {}".format(self.client.user.id))
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_ready()

        @self.client.event
        async def on_resumed():
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_resumed()

        # @self.client.event
        # async def on_error(event, *args, **kwargs):
            # self.logger.error(event)
            # for subroutine_obj in self.subroutines:
                # await subroutine_obj.on_error(event, *args, **kwargs)

        @self.client.event
        async def on_message(message):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_message(message)

        @self.client.event
        async def on_message_delete(message):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_message_delete(message)

        @self.client.event
        async def on_message_edit(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_message_edit(before, after)

        @self.client.event
        async def on_reaction_add(reaction, user):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_reaction_add(reaction, user)

        @self.client.event
        async def on_reaction_remove(reaction, user):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_reaction_remove(reaction, user)

        @self.client.event
        async def on_reaction_clear(message, reactions):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_reaction_clear(message, reactions)

        @self.client.event
        async def on_channel_create(channel):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_channel_create(channel)

        @self.client.event
        async def on_channel_delete(channel):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_channel_delete(channel)

        @self.client.event
        async def on_channel_update(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_channel_update(before, after)

        @self.client.event
        async def on_member_join(member):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_member_join(member)

        @self.client.event
        async def on_member_leave(member):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_member_leave(member)

        @self.client.event
        async def on_member_update(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_member_update(before, after)

        @self.client.event
        async def on_server_join(server):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_join(server)

        @self.client.event
        async def on_server_remove(server):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_remove(server)

        @self.client.event
        async def on_server_update(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_update(before, after)

        @self.client.event
        async def on_server_role_create(role):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_role_delete(role)

        @self.client.event
        async def on_server_role_delete(role):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_role_delete(role)

        @self.client.event
        async def on_server_role_update(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_role_update(before, after)

        @self.client.event
        async def on_server_emojis_update(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_server_emojis_update(before, after)

        @self.client.event
        async def on_voice_state_update(before, after):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_voice_state_update(before, after)

        @self.client.event
        async def on_member_ban(member):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_member_ban(member)

        @self.client.event
        async def on_member_unban(server, user):
            for subroutine_obj in self.subroutines:
                await subroutine_obj.on_member_unban(server, user)

    def load_client(self, client=None):
        asyncio.set_event_loop(asyncio.new_event_loop())
        if not client:
            self.set_client(discord.Client())
            return
        self.set_client(client)

    def load_database(self, db=None):
        if not db:
            self.set_database(database.Database(inherit=self))
            return
        self.set_database(db)

    def load_config(self, config):
        if type(config) is dict:
            self.set_config(config)
            return

        if not os.path.exists(config):
            self.logger.error("the specified configuration file was not found")
            raise FileNotFoundError

        with open(config, "r") as config_file:
            try:
                self.set_config(json.loads(config_file.read()))
            except json.JSONDecodeError:
                logging.error("the specified configuration file is invalid")
                raise exceptions.InvalidConfiguration

        if self.config["bot"]["subroutines"]:
            for subroutine_name in self.config["bot"]["subroutines"]:
                try:
                    self.load_subroutine(subroutine_name)
                except exceptions.SubroutineAlreadyLoaded:
                    pass

    def get_subroutine(self, subroutine_name):
        for subroutine_obj in self.subroutines:
            if subroutine_obj.info["name"] == subroutine_name:
                return subroutine_obj
        return None

    def subroutine_loaded(self, subroutine_name):
        if self.get_subroutine(subroutine_name):
            return True
        return False

    def load_subroutine(self, subroutine_name):
        if self.subroutine_loaded(subroutine_name):
            raise exceptions.SubroutineAlreadyLoaded
        self.subroutines.append(subroutine.get_subroutine(subroutine_name)(inherit=self))

    def unload_subroutine(self, subroutine_name):
        if not self.subroutine_loaded(subroutine_name):
            raise exceptions.SubroutineNotLoaded
        subroutine_obj = self.get_subroutine(subroutine_name)
        self.subroutines.remove(subroutine_obj)

    def start(self):
        self.logger.info("the bot is starting...")
        if not self.client:
            self.logger.error("bot attempted to start without client")
            raise exceptions.ClientNotLoaded

        # load event handlers as soon as we know the client exists
        self.load_event_handlers()

        if not self.database:
            self.logger.warn("bot starting without db file, defaulting to memory")
            self.set_database(database.Database(inherit=self, in_memory=True))
        try:
            for subroutine_name in self.config["bot"]["subroutines"]:
                self.load_subroutine(subroutine_name)
        except exceptions.SubroutineAlreadyLoaded:
            self.logger.warn("duplicate subroutines in configuration file")
        except KeyError:
            self.logger.warn("no default subroutines supplied. skipping...")

        self.client.run(self.config["bot"]["token"])
