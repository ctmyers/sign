from command import Command
import control
import positions
import modes

PRIORITY = '\x30'


class Text(object):
    def __init__(self, message, label='A', position=positions.MIDDLE,
                 mode=modes.HOLD, locked=True):
        self.message = message
        self.label = label
        self.size = max(1, min(len(message), 125))
        self.position = position
        self.mode = modes
        self.locked = control.LOCKED if locked else control.UNLOCKED
        self.command = Command("%s%s%s%s%s%s" % (control.WRITE_TEXT, label,
                                                 control.ESC, position, mode, message))
