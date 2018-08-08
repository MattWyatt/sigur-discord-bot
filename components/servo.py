import inspect
import os
from components import exceptions
from components import component

servo_list = []


def get_servo(name):
    for servo_class in servo_list:
        if servo_class.info["name"] == name:
            return servo_class
    raise exceptions.ServoNonexistent


# decorates a class to assign properties and add it to the servo_list
def add_servo(servo_information):
    # takes the class as the argument
    def register_servo(new_servo):
        class ServoWrapper:
            # static property with information
            info = servo_information
            for file in os.listdir("./augments"):
                if file == "{}.py".format(info["name"]):
                    info["file_path"] = os.path.realpath("./augments/{}".format(file))

            def __init__(self, *args):
                self.wrapped_servo = new_servo(*args)

            def __getattr__(self, name):
                return getattr(self.wrapped_servo, name)

        # append to list and return
        servo_list.append(ServoWrapper)
        return ServoWrapper
    return register_servo


# decorates a command with its information
def add_command(command_information):
    def register_command(func):
        # set a flag to mark the function as a command
        func.is_command = True
        # store the information as an attribute of the function itself
        func.info = command_information
        return func
    return register_command


class Servo(component.Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = []

        method_list = inspect.getmembers(self, inspect.iscoroutinefunction)
        for method in method_list:
            try:
                if method[1].is_command:
                    self.commands.append(method[1])
            except AttributeError:
                pass

        self.setup()

    def setup(self):
        pass

    def has_command(self, command):
        for cmd in self.commands:
            if cmd.info["name"] == command:
                return True
            if "aliases" in cmd.info:
                if command in cmd.info["aliases"]:
                    return True
        return False

    # static method for ensuring user has permissions
    def check_permissions(self, command, context):
        if "permissions" not in command:
            return True
        # generate a dictionary of the user's permissions
        user_perms = dict(iter(context.channel.permissions_for(context.author)))
        required_perms = command["permissions"]
        for perm in required_perms:
            if perm not in user_perms or not user_perms[perm]:
                return False
        return True

    # call a function from a servo by giving it a name and context
    async def call(self, command_name, context):
        self.logger.debug("attempting to call command [{}]...".format(command_name))
        success = False
        for command in self.commands:
            if command.info["name"] == command_name:
                if self.check_permissions(command.info, context):
                    await command(context)
                    success = True
                else:
                    await self.client.send_message(context.channel,
                                                   "you may not perform this command")
            # process aliases
            if "aliases" in command.info:
                if command_name in command.info["aliases"]:
                    if self.check_permissions(command.info, context):
                        await command(context)
                        success = True
                    else:
                        await self.client.send_message(context.channel,
                                                       "you may not perform this command")
        return success
