import re


COMMAND_HANDLED = True
COMMAND_NOT_HANDLED = None


class CommandException(Exception):
    def __init__(self, command_text, message=None, *args, **kwargs):
        super(CommandException, self).__init__(self, message, *args, **kwargs)
        self.command_text = command_text


class UnknownCommandException(CommandException):
    pass


class CommandParser(object):
    """
    Entry point for parsing and executing game commands.
    """
    def parse(self, command_text, controller=None, user=None, world=None):
        """
        Parse the specified string and find the Command and match
        information that can handle it. Returns None if no known
        commands can handle it.
        """
        if command_text.startswith("/"):
            stripped = command_text[1:]
            # Look for a subclass of Command whose format matches command_text
            for command_type in Command.__subclasses__():
                if not hasattr(command_type, "command"):
                    raise Exception("Subclasses of Command must have a command attribute.")
                cmd_regex = command_type.command
                match = re.match(cmd_regex, stripped)
                if match:
                    return command_type(user, world, controller), match
        return None

    def execute(self, command_text, controller=None, user=None, world=None):
        """
        Finds and executes the first command that can handle the specified
        string. If the command has a return value, that value is returned.
        If it does not, then COMMAND_HANDLED is returned. If no commands
        can handle the string, COMMAND_NOT_HANDLED is returned.
        """
        parsed = self.parse(command_text, controller=controller, user=user, world=world)
        if parsed:
            command, match = parsed
            # Pass matched groups to command.execute
            ret = command.execute(*match.groups(), **match.groupdict())
            if ret is None:
                return COMMAND_HANDLED
            else:
                return ret
        else:
            if command_text.startswith("/"):
                raise UnknownCommandException(command_text)
            return COMMAND_NOT_HANDLED


class Command(object):
    command = None
    help_text = None

    def __init__(self, user, world, controller):
        self.user = user
        self.world = world
        self.controller = controller

    def execute(self, *args, **kwargs):
        pass


class GiveBlockCommand(Command):
    command = r"^give (\d+) (\d+)?$"
    help_text = "give <block_id> [amount]: Give a specified amount (default of 1) of the item to the player"

    def execute(self, block_id, amount=1, *args, **kwargs):
        self.user.inventory.add_item(int(block_id), quantity=int(amount))


class SetTimeCommand(Command):
    command = r"^time set (\d+)$"
    help_text = "time set <number>: Set the time of day 00-24"

    def execute(self, time, *args, **kwargs):
        self.controller.time_of_day = int(time)
