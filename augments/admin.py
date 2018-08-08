import discord
from components import servo


def get_and_validate_user(context):
    if not len(context.argv) > 1:
        return
    for member in context.server.members:
        if member.mention == context.args[0]:
            return member
    return


@servo.add_servo({
    "name": "admin",
    "description": "administrative commands to manage a server",
    "author": "Saviour#8988"
})
class Admin(servo.Servo):
    @servo.add_command({
        "name": "kick",
        "permissions": ["kick_members"],
        "description": "kicks the specified user from the server",
        "author": "Saviour#8988"
    })
    async def cmd_kick(self, context):
        kick_member = get_and_validate_user(context)
        if not kick_member:
            await self.client.send_message(context.channel,
                                           "invalid or nonexistent user supplied")
            return
        await self.client.send_message(context.channel,
                                       "kicking {}...".format(kick_member.mention))
        await self.client.kick(kick_member)
        await self.client.send_message(context.channel,
                                       "godspeed you! out of this server.")

    @servo.add_command({
        "name": "ban",
        "permissions": ["ban_members"],
        "description": "bans the specified user from the server",
        "author": "Saviour#8988"
    })
    async def cmd_ban(self, context):
        ban_member = get_and_validate_user(context)
        if not ban_member:
            await self.client.send_message(context.channel,
                                           "invalid or nonexistent user supplied")
            return
        await self.client.send_message(context.channel,
                                       "banning {}...".format(ban_member.mention))
        await self.client.ban(ban_member)
        await self.client.send_message(context.channel,
                                       "godspeed you! out of this server.")

    @servo.add_command({
        "name": "mute",
        "aliases": ["silence", "shutup"],
        "permissions": ["manage_roles"],
        "description": "mutes a user across the entire server",
        "author": "Saviour#8988"
    })
    async def cmd_mute(self, context):
        mute_member = get_and_validate_user(context)
        if not mute_member:
            await self.client.send_message(context.channel,
                                           "invalid or nonexistent user supplied")
            return

        mute_role = None
        # attempt to find the Muted role
        for role in context.server.roles:
            if role.name == "muted":
                mute_role = role

        # if no Muted role was found
        if not mute_role:
            # create empty permission object
            perms = discord.Permissions.none()
            # create the mute role
            mute_role = await self.client.create_role(context.server, name="muted", permissions=perms)
            # create the overwrite and deny sending messages
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            # assign the overwrite to all channels
            for channel in context.server.channels:
                await self.client.edit_channel_permissions(channel, mute_role, overwrite)

        await self.client.add_roles(mute_member, mute_role)
        await self.client.send_message(context.channel,
                                       "muted {}".format(mute_member.mention))

    @servo.add_command({
        "name": "unmute",
        "aliases": ["unsilence", "speak"],
        "permissions": ["manage_roles"],
        "description": "unmutes a user",
        "author": "Saviour#8988"
    })
    async def cmd_unmute(self, context):
        mute_member = get_and_validate_user(context)
        if not mute_member:
            await self.client.send_message(context.channel,
                                           "invalid or nonexistent user supplied")
            return

        mute_role = None
        # attempt to find the Muted role
        for role in context.server.roles:
            if role.name == "muted":
                mute_role = role

        # if no Muted role was found
        if not mute_role:
            await self.client.send_message(context.channel,
                                           "no one has been muted in this server.")
            return
        await self.client.remove_roles(mute_member, mute_role)
        await self.client.send_message(context.channel,
                                       "unmuted {}".format(mute_member.mention))

    @servo.add_command({
        "name": "channelmute",
        "aliases": ["chmute", "chsilence"],
        "description": "mutes a user in the current channel",
        "permissions": ["manage_channels", "manage_messages"],
        "author": "Saviour#8988"
    })
    async def cmd_channelmute(self, context):
        mute_member = get_and_validate_user(context)
        if not mute_member:
            await self.client.send_message(context.channel,
                                           "invalid or nonexistent user supplied")
            return
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        await self.client.edit_channel_permissions(context.channel, mute_member, overwrite)
        await self.client.send_message(context.channel,
                                       "{} has been muted in this channel".format(mute_member.mention))

    @servo.add_command({
        "name": "channelunmute",
        "aliases": ["chunmute", "chspeak"],
        "description": "unmutes any user muted in the current channel",
        "permissions": ["manage_channels", "manage_messages"],
        "author": "Saviour#8988"
    })
    async def cmd_channelunmute(self, context):
        mute_member = get_and_validate_user(context)
        if not mute_member:
            await self.client.send_message(context.channel,
                                           "invalid or nonexistent user supplied")
            return
        await self.client.delete_channel_permissions(context.channel, mute_member)
        await self.client.send_message(context.channel,
                                       "{} has been unmuted in this channel".format(mute_member.mention))