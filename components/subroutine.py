from components import component

# yeah i know i'm reusing the code from the command handler
# leave me alone :(
subroutine_list = []


def get_subroutine(name):
    for subroutine_class in subroutine_list:
        if subroutine_class.info["name"] == name:
            return subroutine_class


# decorates a class to assign properties and add it to the subroutine_list
def add_subroutine(subroutine_information):
    def register_subroutine(new_subroutine):
        class SubroutineWrapper:
            # static property with information
            info = subroutine_information

            def __init__(self, *args, **kwargs):
                self.wrapped_subroutine = new_subroutine(*args, **kwargs)

            def __getattr__(self, name):
                return getattr(self.wrapped_subroutine, name)

        # append to list and return
        subroutine_list.append(SubroutineWrapper)
        return SubroutineWrapper
    return register_subroutine


class Subroutine(component.Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup()

    def setup(self):
        pass

    # metric fuck-ton of virtual functions to be called by bot.Bot
    async def on_ready(self):
        pass

    async def on_resumed(self):
        pass

    async def on_error(self, event, *args, **kwargs):
        pass

    async def on_message(self, message):
        pass

    async def on_message_deleted(self, message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    async def on_reaction_clear(self, message, reactions):
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_leave(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_server_join(self, server):
        pass

    async def on_server_remove(self, server):
        pass

    async def on_server_update(self, before, after):
        pass

    async def on_server_role_create(self, role):
        pass

    async def on_server_role_delete(self, role):
        pass

    async def on_server_role_update(self, role):
        pass

    async def on_server_emojis_update(self, before, after):
        pass

    async def on_voice_state_update(self, before, after):
        pass

    async def on_member_ban(self, member):
        pass

    async def on_member_unban(self, server, user):
        pass
