from command import Command
import control


class String(object):
    def __init__(self, message, label='A', locked=control.LOCKED):
        self.message = message
        self.label = label
        self.size = max(1, min(len(message), 125))
        self.locked = locked
        self.command = Command("%s%s%s" % (control.WRITE_STRING, label,
                                           message))
