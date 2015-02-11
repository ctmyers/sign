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
        self.sock = None

    def connect(self):
        if self.sock:
            self.sock.close()
            self.sock = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def send(self, command):
        if self.sock is None:
            self.connect()

        try:
            # print command
            self.sock.sendall(command.data())
        except socket.error:
            self.connect()

    def __del__(self):
        self.sock.close()
