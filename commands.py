# Imports, sorted alphabetically.

# Python packages
import datetime
import os
import re

# Third-party packages
import pyglet

# Modules from this project
from blocks import BlockID
from items import get_item
import globals as G

COMMAND_HANDLED = True
COMMAND_NOT_HANDLED = None
COMMAND_INFO_COLOR = (41, 125, 255, 255)
COMMAND_ERROR_COLOR = (255, 0, 0, 255)


class CommandException(Exception):
    def __init__(self, command_text, message=None, *args, **kwargs):
        super(CommandException, self).__init__(self, message, *args, **kwargs)
        self.command_text = command_text
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, self.message)


class UnknownCommandException(CommandException):
    def __init__(self, command_text, *args, **kwargs):
        super(UnknownCommandException, self).__init__(command_text, *args, **kwargs)
        self.message = "Unrecognized command: %s" % self.command_text


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
            stripped = command_text[1:].strip()
            # Look for a subclass of Command whose format matches command_text
            for command_type in Command.__subclasses__():
                if not hasattr(command_type, "command"):
                    raise Exception("Subclasses of Command must have a command attribute.")
                cmd_regex = command_type.command
                match = re.match(cmd_regex, stripped)
                if match:
                    instance = command_type(stripped, user, world, controller)
                    return instance, match
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
            # ...but filter out "None" arguments. If commands
            # want optional arguments, they should use keyword arguments
            # in their execute methods.
            args = filter(lambda a: a is not None, match.groups())
            kwargs = {}
            for key, value in match.groupdict().iteritems():
                if value is not None:
                    kwargs[key] = value
            ret = command.execute(*args, **kwargs)
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

    def __init__(self, command_text, user, world, controller):
        self.command_text = command_text
        self.user = user
        self.world = world
        self.controller = controller

    def execute(self, *args, **kwargs):
        pass

    def send_info(self, text):
        self.controller.write_line(text, color=COMMAND_INFO_COLOR)

    def send_error(self, text):
        self.controller.write_line(text, color=COMMAND_ERROR_COLOR)


class HelpCommand(Command):
    command = r"^help$"
    help_text = "help: Show this help information"

    def execute(self, *args, **kwargs):
        self.send_info("****** Available Commands ******")
        for command_type in Command.__subclasses__():
            if hasattr(command_type, 'help_text') and command_type.help_text:
                self.send_info(command_type.help_text)


class GiveBlockCommand(Command):
    command = r"^give (\d+(?:[\.,]\d+)?)(?:\s+(\d+))?$"
    help_text = "give <block_id> [amount]: Give a specified amount (default of 1) of the item to the player"

    def execute(self, block_id, amount=1, *args, **kwargs):
        try:
            bid = BlockID(block_id)
            item_or_block = get_item(float("%s.%s" % (bid.main, bid.sub)))
            self.send_info("Giving %s of '%s'." % (amount, item_or_block.name))
            self.user.inventory.add_item(bid, quantity=int(amount))
            self.controller.item_list.update_items()
            self.controller.inventory_list.update_items()
        except KeyError:
            raise CommandException(self.command_text, message="ID %s unknown." % block_id)
        except ValueError:
            raise CommandException(self.command_text, message="ID should be a number. Amount must be an integer.")


class SetTimeCommand(Command):
    command = r"^time set (\d+)$"
    help_text = "time set <number>: Set the time of day 00-24"

    def execute(self, time, *args, **kwargs):
        try:
            tod = int(time)
            if 0 <= tod <= 24:
                self.send_info("Setting time to %s" % tod)
                self.controller.time_of_day = tod
            else:
                raise ValueError
        except ValueError:
            raise CommandException(self.command_text, message="Time should be a number between 0 and 24")


class GetIDCommand(Command):
    command = r"^id$"
    help_text = "id: Get the id of the active item"

    def execute(self, *args, **kwargs):
        current = self.controller.item_list.get_current_block()
        if current:
            self.send_info("ID: %s" % current.id)
        else:
            self.send_info("ID: None")


class TakeScreencapCommand(Command):
    command = r"^screencap$"
    help_text = "screencap: saves current screen to a file. Press " + G.SCREENCAP_KEY + " for instant screencap."


    def execute(self, *args, **kwargs):
        now = datetime.datetime.now()
        dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        st = dt.strftime('%Y-%m-%d_%H.%M.%S')
        filename = str(st) + '.png'
        if not os.path.exists('screencaptures'):
            os.makedirs('screencaptures')

        # Hide inputs so they're not on the screencapture
        self.controller.text_input.visible = False
        self.controller.chat_box.visible = False
        self.controller.on_draw()

        path = 'screencaptures/' + filename
        pyglet.image.get_buffer_manager().get_color_buffer().save(path)
        self.send_info("Screen capture saved to '%s'" % path)

        # ...and then show them again
        self.controller.text_input.visible = True
        self.controller.chat_box.visible = True