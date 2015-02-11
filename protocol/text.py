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

        if type(messages) == Page:
            self.message = messages.content
        elif type(messages) == str:
            self.message = Page(messages).content
        else:
            self.message = ''.join(m.content if type(m) == Page
                                   else Page(m).content
                                   for m in messages)

        self.size = max(1, min(len(self.message), 125))
        self.locked = control.LOCKED if locked else control.UNLOCKED
        self._command = "%s%s%s" % (control.WRITE_TEXT,
                                    self.label, self.message)


class Page(object):
    def __init__(self, message, position=positions.MIDDLE, mode=modes.HOLD):
        self.message = message
        self.position = position
        self.mode = mode

        self.content = '%s%s%s%s' % (control.ESC, self.position,
                                     self.mode, self.message)
