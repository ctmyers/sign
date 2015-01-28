from command import Command
from text import Text
from string import String
import control


class MemoryConfig(object):
        def __init__(self, files=None):
            if files:
                contents_list = []
                for f in files:
                    if type(f) == Text:
                        file_type = 'A'
                        extra = 'FFFF'
                    elif type(f) == String:
                        file_type = 'A'
                        extra = '0000'
                    else:
                        # dots
                        raise ValueError('unsupported file type')
                    contents_list.append('%s%s%s%s%s' % (f.label, file_type,
                                                         f.locked, f.size,
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