import discord
from datetime import datetime
from components import servo
from components import subroutine


@servo.add_servo({
    "name": "overseermanager",
    "description": "controls the overseer",
    "author": "Saviour#8988"
})
class OverseerManager(servo.Servo):
    def setup(self):
        overseer_schema = {
            "server": "CHAR(18)",
            "channel": "CHAR(18)"
        }
        self.database.make_table("overseer", overseer_schema)

    @servo.add_command({
        "name": "enableoverseer",
        "aliases": ["eos"],
        "permissions": ["administrator"],
        "description": "enables overseer logging in this channel",
        "author": "Saviour#8988"
    })
    async def enable_overseer(self, context):
        channel = self.database.retrieve_from_table("overseer", "server", context.server.id)
        if not channel:
            self.database.insert_into_table("overseer", context.server.id, context.channel.id)
            embed = discord.Embed(type="rich",
                                  title="logging enabled in this channel",
                                  color=discord.Color.green())
            embed.set_footer(text=str(context.timestamp))
            await self.client.send_message(context.channel, embed=embed)
            return
        embed = discord.Embed(type="rich",
                              title="logging is already enabled for this server",
                              color=discord.Color.red())
        embed.set_footer(text=str(context.timestamp))
        await self.client.send_message(context.channel, embed=embed)

    @servo.add_command({
        "name": "disableoverseer",
        "permissions": ["administrator"],
        "description": "disables the overseer in this server",
        "author": "Saviour#8988"
    })
    async def disable_overseer(self, context):
        channel = self.database.retrieve_from_table("overseer", "server", context.server.id)
        if channel:
            self.database.delete_from_table("overseer", "server", context.server.id)
            embed = discord.Embed(type="rich",
                                  title="logging has been disabled for this server",
                                  color=discord.Color.green())
            embed.set_footer(text=str(datetime.utcnow()))
            await self.client.send_message(context.channel, embed=embed)
            return
        embed = discord.Embed(type="rich",
                              title="logging was never enabled for this server",
                              color=discord.Color.red())
        embed.set_footer(text=str(datetime.utcnow()))
        await self.client.send_message(context.channel, embed=embed)


def grab_embed(title):
    embed = discord.Embed(type="rich",
                          title=title,
                          color=discord.Color.green())
    embed.set_footer(text=str(datetime.utcnow()))
    return embed


@subroutine.add_subroutine({
    "name": "overseer",
    "description": "watches and logs server activities",
    "author": "Saviour#8988"
})
class Overseer(subroutine.Subroutine):
    def setup(self):
        overseer_schema = {
            "server": "CHAR(18)",
            "channel": "CHAR(18)"
        }
        self.database.make_table("overseer", overseer_schema)

    def log_check(self, server_id):
        if self.database.retrieve_from_table("overseer", "server", server_id):
            return True
        return False

    def get_channel(self, server_id):
        channel = self.database.retrieve_from_table("overseer", "server", server_id)[0][1]
        return self.client.get_channel(channel)

    async def on_ready(self):
        channels = self.database.retrieve_all_from_table("overseer")
        embed = discord.Embed(type="rich",
                              title="bot restarted",
                              color=discord.Color.green())
        embed.set_footer(text=str(datetime.utcnow()))
        for entry in channels:
            channel = await self.client.get_channel(entry[1])
            if channel:
                await self.client.send_message(channel, embed=embed)

    async def on_message_delete(self, message):
        if not self.log_check(message.server.id):
            return

        embed = grab_embed("message deleted")
        embed.add_field(name="channel", value=message.channel.mention, inline=False)
        if message.content:
            embed.add_field(name="content", value=message.content, inline=False)
        embed.add_field(name="id", value=message.id, inline=False)
        if message.attachments:
            current = 1
            for attachment in message.attachments:
                attachment = attachment["proxy_url"]
                embed.add_field(name="attachment {}".format(str(current)), value=attachment, inline=False)
                current += 1
        await self.client.send_message(self.get_channel(message.server.id), embed=embed)

    async def on_message_edit(self, before, after):
        if not self.log_check(before.server.id):
            return

        if before.author.bot:
            return

        embed = grab_embed("message edited")
        embed.add_field(name="channel", value=before.channel.mention, inline=False)
        if before.content:
            embed.add_field(name="original", value=before.content, inline=False)
        if after.content:
            embed.add_field(name="edited", value=after.content, inline=False)
        embed.add_field(name="id", value=before.id, inline=False)
        await self.client.send_message(self.get_channel(before.server.id), embed=embed)

    async def on_channel_create(self, channel):
        if not self.log_check(channel.server.id):
            return

        embed = grab_embed("channel created")
        embed.add_field(name="name", value=channel.mention, inline=False)
        embed.add_field(name="id", value=channel.id, inline=False)
        await self.client.send_message(self.get_channel(channel.server.id), embed=embed)

    async def on_channel_delete(self, channel):
        if not self.log_check(channel.server.id):
            return

        embed = grab_embed("channel deleted")
        embed.add_field(name="name", value=channel.name, inline=False)
        embed.add_field(name="id", value=channel.id, inline=False)
        await self.client.send_message(self.get_channel(channel.server.id), embed=embed)

    async def on_channel_update(self, before, after):
        if not self.log_check(before.server.id):
            return

        embed = grab_embed("channel updated")

        if not before.name == after.name:
            embed.add_field(name="original name", value=before.name)
            embed.add_field(name="new name", value=after.mention, inline=False)

        embed.add_field(name="id", value=before.id)

        if not before.topic == after.topic:
            if not before.topic:
                embed.add_field(name="original topic", value="**no topic set**", inline=False)
            else:
                embed.add_field(name="original topic", value=before.topic, inline=False)
            if not after.topic:
                embed.add_field(name="new topic", value="**no topic set**", inline=False)
            else:
                embed.add_field(name="new topic", value=after.topic, inline=False)

        if not before.name == after.name or not before.topic == after.topic:
            await self.client.send_message(self.get_channel(before.server.id), embed=embed)

        overwrites_updated = True
        if len(before.overwrites) == len(after.overwrites):
            overwrites_updated = False
            for b_overwrite, a_overwrite in zip(before.overwrites, after.overwrites):
                if not b_overwrite[0] == a_overwrite[0]:
                    overwrites_updated = True
                if not b_overwrite[1].pair() == a_overwrite[1].pair():
                    overwrites_updated = True

        if overwrites_updated:
            embed = grab_embed("channel permissions updated")
            embed.add_field(name="channel", value=after.mention)
            await self.client.send_message(self.get_channel(before.server.id), embed=embed)

    async def on_member_join(self, member):
        if not self.log_check(member.server.id):
            return

        embed = grab_embed("user joined")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="username", value=member.mention, inline=False)
        embed.add_field(name="id", value=member.id, inline=False)
        embed.add_field(name="user joined server", value=str(datetime.utcnow()))
        embed.add_field(name="user joined discord", value=str(member.created_at))
        await self.client.send_message(self.get_channel(member.server.id), embed=embed)

    async def on_member_leave(self, member):
        if not self.log_check(member.server.id):
            return

        embed = grab_embed("user left")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="username", value=member.mention, inline=False)
        embed.add_field(name="id", value=member.id, inline=False)
        await self.client.send_message(self.get_channel(member.server.id), embed=embed)

    async def on_member_update(self, before, after):
        if not self.log_check(before.server.id):
            return

        avatar_updated = not before.avatar == after.avatar
        nick_updated = not before.nick == after.nick
        roles_updated = not before.roles == after.roles

        if avatar_updated:
            embed = grab_embed("user avatar changed")
            embed.set_thumbnail(url=after.avatar_url)
            embed.add_field(name="username", value=before.mention, inline=False)
            embed.add_field(name="id", value=before.id, inline=False)
            await self.client.send_message(self.get_channel(before.server.id), embed=embed)

        if nick_updated:
            embed = grab_embed("user nickname changed")
            embed.add_field(name="username", value=before.mention, inline=False)
            embed.add_field(name="id", value=before.id, inline=False)
            embed.add_field(name="original nickname", value=before.nick, inline=False)
            embed.add_field(name="new nickname", value=after.nick, inline=False)
            await self.client.send_message(self.get_channel(before.server.id), embed=embed)

        if roles_updated:
            embed = grab_embed("user roles updated")
            embed.add_field(name="username", value=before.mention, inline=False)
            embed.add_field(name="id", value=before.id, inline=False)
            await self.client.send_message(self.get_channel(before.server.id), embed=embed)

    async def on_server_role_create(self, role):
        if not self.log_check(role.server.id):
            return

        embed = grab_embed("role created")
        embed.add_field(name="role", value=role.mention, inline=False)
        embed.add_field(name="id", value=role.id, inline=False)
        await self.client.send_message(self.get_channel(role.server.id), embed=embed)

    async def on_server_role_delete(self, role):
        if not self.log_check(role.server.id):
            return

        embed = grab_embed("role deleted")
        embed.add_field(name="role", value=role.name, inline=False)
        embed.add_field(name="id", value=role.id, inline=False)

    async def on_server_role_update(self, before, after):
        if not self.log_check(before.server.id):
            return

        embed = grab_embed("role updated")
        embed.add_field(name="role", value=before.mention, inline=False)
        embed.add_field(name="id", value=before.id, inline=False)

    async def on_member_ban(self, member):
        if not self.log_check(member.server.id):
            return

        embed = grab_embed("user banned")
        embed.add_field(name="username", value=member.name, inline=False)
        embed.add_field(name="id", value=member.id, inline=False)

    async def on_member_unban(self, server, member):
        if not self.log_check(server.id):
            return

        embed = grab_embed("user unbanned")
        embed.add_field(name="username", value=member.name, inline=False)
        embed.add_field(name="id", value=member.id, inline=False)
