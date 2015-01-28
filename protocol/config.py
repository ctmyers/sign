import json
import os
import sys


class Config(object):
    def __init__(self, path):
        data = Config._load_config(path)
        self.data = Config._parse_config(data)

        self.ip = self.value('ip')
        self.port = self.value('port')
        self.typecode = self.value('typecode', 'Z')
        self.address = self.value('address', '00')

    def value(self, key, default=None):
        if key in self.data:
            return self.data[key]
        else:
            if default:
                return default
            else:
                raise KeyError(key + ' not defined in config file')

    @staticmethod
    def _parse_config(lines):
        stripped_config = ''
        for line in lines:
            line = line.strip()

            comment = line.find('#')
            if comment > -1:
                line = line[:comment]

            if len(line) > 0:
                stripped_config += line

        try:
            data = {key.encode('ascii') if isinstance(key, unicode) else key:
                    value.encode('ascii') if isinstance(value, unicode) else value
                    for key, value in json.loads(stripped_config).iteritems()}
        except ValueError:
            # import traceback
            # traceback.print_exc()
            raise ValueError('failed to parse config file')

        return data

    @staticmethod
    def _load_config(path):
        with open(path, 'r') as config_file:
            return config_file.readlines()


config_path = 'config.rc'
if not os.path.exists(config_path):
    config_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'config.rc')
if not os.path.exists(config_path):
    config_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), '../config.rc')
if not os.path.exists(config_path):
    raise IOError('Could not find config file')

config = Config(config_path)
