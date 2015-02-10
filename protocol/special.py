from command import Command
from text import Text
from string import String
from dots import Dots
import control


class MemoryConfig(object):
        def __init__(self, files=None):
            if files:
                contents_list = []
                for f in files:
                    if type(f) == Text:
                        file_type = 'A'
                        size = '%04X' % f.size
                        extra = 'FFFF'
                    elif type(f) == String:
                        file_type = 'A'
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

            self.command = Command("%s%s%s" % (control.WRITE_SPECIAL, '$', contents))


class RunSequence(object):
    def __init__(self, files=None, locked=True):
        order = 'T'
        locked = control.LOCKED if locked else control.UNLOCKED
        contents = ''.join([f.label for f in files])
        self.command = Command('%s%s%s%s%s' % (control.WRITE_SPECIAL, '.',
                                               order, locked, contents))