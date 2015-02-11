from command import Command
import control
import positions
import modes

PRIORITY = '\x30'


class Text(Command):
    def __init__(self, messages, label='A', locked=True):
        Command.__init__(self)

        self.messages = messages
        self.label = label

        if type(messages) == Message:
            self.message = messages.data
        elif type(messages) == str:
            self.message = Message(messages).data
        else:
            self.message = ''.join(m.data if type(m) == Message
                                   else Message(m).data
                                   for m in messages)

        self.size = max(1, min(len(self.message), 125))
        self.locked = control.LOCKED if locked else control.UNLOCKED
        self._command = "%s%s%s" % (control.WRITE_TEXT,
                                    self.label, self.message)


class Message(object):
    def __init__(self, message, position=positions.MIDDLE, mode=modes.HOLD):
        self.message = message
        self.position = position
        self.mode = mode

        self.data = '%s%s%s%s' % (control.ESC, self.position,
                                  self.mode, self.message)
