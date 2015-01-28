from command import Command
import control


class String(object):
    def __init__(self, message, label='A'):
        self.message = message
        self.label = label
        self.command = Command("%s%s%s" % (control.WRITE_STRING, label,
                                           message))