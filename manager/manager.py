from Queue import Queue
from yapsy.PluginManager import PluginManager
from protocol.special import MemoryConfig
import protocol.interface
import schedule


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

        plugins = plugin_manager.getAllPlugins()
        for p in plugins:
            plugin = p.plugin_object
            self.allocate_labels(plugin)

            configs += plugin.to_config()
            self.command_queue.put(plugin.command_text())

        interface.send(MemoryConfig(configs).command)

        interface.send(self.command_queue.get())

    def allocate_labels(self, plugin):

        def get_labels(labels, count):
            if len(labels) < count:
                raise ValueError('could not allocate file label (too many messages)')
            return tuple(labels.pop(0) for _ in range(count))

        plugin.set_labels(get_labels(self.al_text, 1)[0],
                          get_labels(self.al_string, plugin.string_count()),
                          get_labels(self.al_dots, plugin.dots_count()))
