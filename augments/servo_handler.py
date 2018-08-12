import importlib.util
from components import exceptions
from components import servo
from components import subroutine
from components import contextualizer


@servo.add_servo({
    "name": "servoloader",
    "description": "responsible for loading servos via command",
    "author": "Saviour#8988"
})
class ServoLoader(servo.Servo):
    @servo.add_command({
        "name": "loadservo",
        "aliases": ["ls"],
        "description": "loads a servo into the bot",
        "author": "Saviour#8988"
    })
    async def load_servo(self, context):
        if len(context.argv) <= 1:
            await self.client.send_message(context.channel,
                                           "no servo supplied")
            return

        servo_handler = self.bot.get_subroutine("servohandler")
        if servo_handler:
            if servo_handler.load_servo(context.args[0]):
                await self.client.send_message(context.channel,
                                               "loaded servo `{}`".format(context.args[0]))
                return
            await self.client.send_message(context.channel,
                                           "invalid servo `{}` supplied".format(context.args[0]))

    @servo.add_command({
        "name": "unloadservo",
        "aliases": ["uls"],
        "description": "unloads a servo from the bot",
        "author": "Saviour#8988"
    })
    async def unload_servo(self, context):
        if len(context.argv) <= 1:
            await self.client.send_message(context.channel,
                                           "no servo supplied")
            return

        servo_handler = self.bot.get_subroutine("servohandler")
        if servo_handler:
            if servo_handler.unload_servo(context.args[0]):
                await self.client.send_message(context.channel,
                                               "unloaded servo `{}`".format(context.args[0]))
                return
            await self.client.send_message(context.channel,
                                           "invalid servo `{}` supplied".format(context.args[0]))

    @servo.add_command({
        "name": "refreshservo",
        "aliases": ["rs"],
        "description": "completely refreshes a servo",
        "author": "Saviour#8988"
    })
    async def refresh_servo(self, context):
        if len(context.argv) <= 1:
            await self.client.send_message(context.channel,
                                           "no servo supplied")
            return

        servo_handler = self.bot.get_subroutine("servohandler")
        if servo_handler:
            if servo_handler.refresh_servo(context.args[0]):
                await self.client.send_message(context.channel,
                                               "refreshed servo `{}`".format(context.args[0]))
                return
            await self.client.send_message(context.channel,
                                           "invalid servo `{}` supplied".format(context.args[0]))


@subroutine.add_subroutine({
    "name": "servohandler",
    "description": "responsible for the functionality of servos",
    "author": "Saviour#8988"
})
class ServoHandler(subroutine.Subroutine):
    def setup(self):
        self.servos = []

    def servo_loaded(self, servo_name):
        for servo_obj in self.servos:
            if servo_obj.info["name"] == servo_name:
                return True
        return False

    def load_servo(self, servo_name):
        if self.servo_loaded(servo_name):
            raise exceptions.ServoAlreadyLoaded
        try:
            servo_class = servo.get_servo(servo_name)
        except exceptions.ServoNonexistent:
            return False
        self.servos.append(servo_class(self))
        return True

    def unload_servo(self, servo_name):
        if not self.servo_loaded(servo_name):
            raise exceptions.ServoNotLoaded
        for servo_obj in self.servos:
            if servo_obj.info["name"] == servo_name:
                self.servos.remove(servo_obj)
                return True
        return False

    def refresh_servo(self, servo_name):
        file_path = None
        success_obj_remove = False
        success_class_remove = False
        for servo_obj in self.servos:
            if servo_obj.info["name"] == servo_name:
                file_path = servo_obj.info["file_path"]
                self.servos.remove(servo_obj)
                success_obj_remove = True
        if not file_path:
            raise exceptions.ServoNotLoaded
        for servo_class in servo.servo_list:
            if servo_class.info["name"] == servo_name:
                servo.servo_list.remove(servo_class)
                success_class_remove = True
        if success_obj_remove and success_class_remove:
            print(file_path)
            spec = importlib.util.spec_from_file_location(servo_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.load_servo(servo_name)
            return True
        return False

    async def on_ready(self):
        self.load_servo("servoloader")
        try:
            self.config["bot"]["servos"]
        except KeyError:
            self.logger.info("no starting servos supplied. skipping...")
            return
        for servo_name in self.config["bot"]["servos"]:
            self.logger.info("attempting to load servo {}".format(servo_name))
            try:
                self.load_servo(servo_name)
            except exceptions.ServoNonexistent:
                self.logger.warn("servo {} does not exist!".format(servo_name))

    async def on_message(self, message):
        if message.author.bot:
            return
        context = contextualizer.Contextualizer(message, inherit=self)
        if context.is_command:
            for s in self.servos:
                if s.has_command(context.cmd):
                    self.logger.info("user [{}] issued command [{}]".format(context.author,
                                                                            context.cmd))
                    await s.call(context.cmd, context)
