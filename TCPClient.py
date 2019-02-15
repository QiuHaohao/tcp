import socket
from .TCPTransmitter import TCPTransmitter

class TCPClient(TCPTransmitter):
    def __init__(self, *args):
        super(TCPClient, self).__init__(*args)
        self.socket = None

    def _setup_connection(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print ("Trying to connect to server")
        self.socket.connect((self.ip, self.port))
        print ("Connected! Connection address: ",self.socket)

    def _close_connection(self):
        if self.socket:
            self.socket.close()
            print ("Closed client socket")

    def _send(self, bytes):
        return self.socket.send(bytes)

    def _recv(self):
        BUFF_SIZE = 1024
        data = b''
        while True:
            part = self.socket.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data

if __name__ == "__main__":
    import time
    import os
    c = TCPClient("localhost", 50000)
    c.init_connection()
    while True:
        b = os.urandom(300)
        c.send(b)
        print("Client sent: {}".format(b))
        msg = c.recv()
        print("Client received: {}".format(msg))
        time.sleep(1)