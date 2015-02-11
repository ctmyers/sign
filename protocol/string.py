from command import Command
import control


class String(Command):
    def __init__(self, message, label='A', size=None, locked=True):
        Command.__init__(self)

        self.message = message
        self.label = label
        self.size = size if size else max(1, min(len(message), 125))
        self.locked = control.LOCKED if locked else control.UNLOCKED
        self._command = "%s%s%s" % (control.WRITE_STRING, label,
                                    message)

    @staticmethod
    def call(label):
        return control.CALL_STRING + label
