from command import Command
import control


class String(object):
    def __init__(self, message, label='A', locked=True):
        self.message = message
        self.label = label
        self.size = max(1, min(len(message), 125))
        self.locked = control.LOCKED if locked else control.UNLOCKED
        self.command = Command("%s%s%s" % (control.WRITE_STRING, label,
                                           message))

    @staticmethod
    def call(label):
        return control.CALL_STRING + label
