from Queue import Queue
from yapsy.PluginManager import PluginManager
from protocol.special import MemoryConfig, RunSequence
from datetime import datetime

import time
from threading import Thread
import schedule


def log(string):
    n = datetime.now()
    print '[%02d:%02d:%02d] %s' % (n.hour, n.minute, n.second, string)


class Manager(object):
    def __init__(self, interface):
        self.interface = interface
        self.al_text = [chr(x) for x in range(0x20, 0x7F) if x not in [0x30]]
        self.al_string = [chr(x) for x in range(0x20, 0x7F) if x not in [0x30, 0x3F]]
        self.al_dots = [chr(x) for x in range(0x20, 0x7F)]

        self.command_queue = Queue()

        plugin_manager = PluginManager()
        plugin_manager.setPluginPlaces(['../plugins', './plugins'])
        plugin_manager.collectPlugins()

        configs = []
        sequence = []

        plugins = plugin_manager.getAllPlugins()
        for p in plugins:
            log('loaded plugin %s' % p.name)
            self.allocate_labels(p.plugin_object)

            configs += p.plugin_object.to_config()
            p.plugin_object.schedule.do(self.update, p)

            text = p.plugin_object.text_command()
            sequence.append(text)
            self.command_queue.put(text)
            self.update(p)

        interface.send(MemoryConfig(configs))
        interface.send(RunSequence(sequence))

    def allocate_labels(self, plugin):

        def get_labels(labels, count):
            if len(labels) < count:
                raise ValueError('could not allocate file label (too many messages)')
            return tuple(labels.pop(0) for _ in range(count))

        plugin.set_labels(get_labels(self.al_text, 1)[0],
                          get_labels(self.al_string, plugin.string_count()),
                          get_labels(self.al_dots, plugin.dots_count()))

    def update(self, plugin):
        def get_commands():
            for c in plugin.plugin_object.get_commands():
                self.command_queue.put(c)

        log('updating %s' % plugin.name)
        thread = Thread(target=get_commands)
        thread.start()

    def send_commands(self):
        while True:
            if not self.command_queue.empty():
                self.interface.send(self.command_queue.get())
            else:
                time.sleep(1)

    def run(self):
        s = Thread(target=self.send_commands)
        s.daemon = True
        s.start()

        while True:
            schedule.run_pending()
            time.sleep(1)
