from config import config


class Interface(object):
    def __init__(self, ip=config.ip, port=config.port):
        self.ip = ip
        self.port = port

    def send(self, command):
        return False


import socket


class NetworkInterface(Interface):
    def __init__(self, ip=config.ip, port=config.port):
        super(NetworkInterface, self).__init__(ip, port)

    def send(self, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        sock.send(command.data)
        sock.close()
