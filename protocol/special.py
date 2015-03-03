from command import Command
from text import Text
from string import String
from dots import Dots
import control

from datetime import datetime


class MemoryConfig(Command):
    def __init__(self, files=None):
        Command.__init__(self)

        if files:
            contents_list = []
            for f in files:
                if type(f) == Text:
                    file_type = 'A'
                    size = '%04X' % f.size
                    extra = 'FFFF'
                elif type(f) == String:
                    file_type = 'B'
                    size = '%04X' % f.size
                    extra = '0000'
                elif type(f) == Dots:
                    file_type = 'D'
                    size = '%02X%02X' % (f.height, f.width)
                    extra = '2000'
                else:
                    raise TypeError('invalid file type')
                contents_list.append('%s%s%s%s%s' % (f.label,
                                                     file_type,
                                                     f.locked,
                                                     size,
                                                     extra))
            contents = ''.join(contents_list)
        else:
            contents = ''

        self._command = "%s%s%s" % (control.WRITE_SPECIAL, '$', contents)


class RunSequence(Command):
    def __init__(self, files=None, locked=True):
        Command.__init__(self)

        order = 'T'
        locked = control.LOCKED if locked else control.UNLOCKED
        contents = ''.join([f.label for f in files])
        self._command = '%s%s%s%s%s' % (control.WRITE_SPECIAL, '.',
                                        order, locked, contents)


class TimeOfDay(Command):
    def __init__(self, time=datetime.now()):
        Command.__init__(self)
        self._command = '%s%s%02d%02d' % (control.WRITE_SPECIAL, ' ',
                                          time.hour, time.minute)


class DayOfWeek(Command):
    def __init__(self, time=datetime.now()):
        Command.__init__(self)
        day = time.isoweekday() + 1
        if day > 7:
            day -= 7
        self._command = '%s%s%s' % (control.WRITE_SPECIAL, '&', day)


class Date(Command):
    def __init__(self, time=datetime.now()):
        Command.__init__(self)

        self._command = '%s%s%02d%02d%02d' % (control.WRITE_SPECIAL, ';',
                                              time.month, time.day, time.year % 100)
