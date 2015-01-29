from yapsy.PluginManager import PluginManager
import schedule


class Manager(object):
    def __init__(self):
        plugin_manager = PluginManager()
        plugin_manager.setPluginPlaces(['../plugins', './plugins'])
        plugin_manager.collectPlugins()