# is this really how you do exception files?
# just a bunch of empty classes?
# i dunno but i'm goin with it


# base exception class
class BotException(Exception):
    pass


class BotAlreadyExists(BotException):
    pass


class BotNonexistent(BotException):
    pass


class ClientNotLoaded(BotException):
    pass


class InvalidConfiguration(BotException):
    pass


class SubroutineAlreadyLoaded(BotException):
    pass


class SubroutineNotLoaded(BotException):
    pass


class ServoAlreadyLoaded(BotException):
    pass


class ServoNotLoaded(BotException):
    pass


class ServoNonexistent(BotException):
    pass
