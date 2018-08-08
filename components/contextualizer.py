import inspect
from components import component


class Contextualizer(component.Component):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._is_command = message.content.startswith(self.config["bot"]["prefix"])
        self.message = message
        # set all the properties of message to itself
        for member in inspect.getmembers(self.message):
            # the members we want conveniently start without an underscore
            if not member[0].startswith("_"):
                self.__setattr__(member[0], member[1])

    @property
    def is_command(self):
        return self._is_command

    @property
    def argv(self):
        argv = self.content[len(self.config["bot"]["prefix"]):].split(" ")
        return argv

    @property
    def cmd(self):
        return self.argv[0]

    @property
    def args(self):
        return self.argv[1:]

