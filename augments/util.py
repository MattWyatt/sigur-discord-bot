import calendar
import datetime
import discord
from components import servo


def search_user(user, server):
    for member in server.members:
        if member.name == user or member.mention == user or user.id == user:
            return member
    return False


@servo.add_servo({
    "name": "util",
    "description": "utility commands for miscellaneous tasks",
    "author": "Saviour#8988"
})
class Util(servo.Servo):

    @servo.add_command({
        "name": "help",
        "aliases": ["h", "sos"],
        "description": "displays all commands and their usages",
        "author": "Saviour#8988"
    })
    async def help(self, context):
        help_string = ""
        help_title = ""
        servo_list = []
        for subroutine_obj in self.bot.subroutines:
            if subroutine_obj.info["name"] == "servohandler":
                for servo_obj in subroutine_obj.servos:
                    servo_list.append(servo_obj)
        if len(context.argv) == 1:
            help_title += "currently loaded servos"
            prefix = self.config["bot"]["prefix"]
            help_string += "type `{}help [servo name]` to get more information\n\n".format(prefix)
            for servo_obj in servo_list:
                help_string += "**{}**".format(servo_obj.info["name"])
                help_string += " - {}\n".format(servo_obj.info["description"])
        else:
            for servo_obj in servo_list:
                if servo_obj.info["name"] == context.argv[1]:
                    help_title += "commands for `{}`".format(servo_obj.info["name"])
                    for command in servo_obj.commands:
                        help_string += "**{}**".format(command.info["name"])
                        help_string += " - {}\n".format(command.info["description"])
        embed = discord.Embed(type="rich",
                              title=help_title,
                              description=help_string,
                              color=discord.Color.green())
        await self.client.send_message(context.channel, embed=embed)

    @servo.add_command({
        "name": "userinfo",
        "aliases": ["uinfo"],
        "description": "displays information about a user",
        "author": "Saviour#8988"
    })
    async def user_info(self, context):
        if context.args[0] == "":
            user = context.author
        else:
            user = search_user(context.args[0], context.server)
            if not user:
                await self.client.send_message(context.channel, "user `{}` not found".format(context.args[0]))
                return
        role_array = user.roles
        roles = []
        for role in role_array:
            if role.name == "@everyone":
                roles.append(role.name)
            else:
                roles.append(role.mention)
        roles.reverse()
        join_date = user.joined_at
        user_information = {
            "Username": user.name + "#" + user.discriminator,
            "Joined On": "{}, {} {}".format(calendar.month_name[join_date.month], join_date.day, join_date.year),
            "Roles": "\n".join(str(x) for x in roles),
            "Playing": user.game,
        }
        embed = discord.Embed(type="rich")
        embed.set_thumbnail(url=user.avatar_url)
        for key in user_information:
            embed.add_field(name=key, value=user_information[key])
        await self.client.send_message(context.channel, embed=embed)

    @servo.add_command({
        "name": "serverinfo",
        "aliases": ["sinfo"],
        "description": "retrieves info about the server",
        "author": "Saviour#8988"
    })
    async def server_info(self, context):
        embed = discord.Embed(type="rich")
        # set the thumbnail to the server icon
        embed.set_thumbnail(url=context.server.icon_url)
        embed.set_footer(text="Server ID: {}".format(context.server.id))
        created = context.server.created_at
        now = datetime.datetime.now()
        server_information = {
            "Name": context.server.name,
            "Region": context.server.region,
            "Members": context.server.member_count,
            "Roles": str(len(context.server.roles)),
            "Created": "{}, {}, {} at {}:{} UTC | {} days ago".format(calendar.month_name[created.month],
                                                                      created.day,
                                                                      created.year,
                                                                      created.hour,
                                                                      created.minute,
                                                                      (now - created).days)
        }
        for key in server_information:
            embed.add_field(name=key, value=server_information[key])
        await self.client.send_message(context.channel, embed=embed)

    @servo.add_command({
        "name": "say",
        "description": "repeats after you",
        "author": "Saviour#8988"
    })
    async def say(self, context):
        await self.client.send_message(context.channel, " ".join(context.args))

