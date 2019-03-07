import socket
from .TCPTransmitter import TCPTransmitter

class TCPServer(TCPTransmitter):
    def __init__(self, *args):
        super(TCPServer, self).__init__(*args)
        self.socket = None
        self.client = None
        self.addr = None

    def _setup_connection(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # allow reuse of IP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.socket.bind((self.ip,self.port))
        self.socket.listen(1)
        print (
            "Listening for incoming TCP connections on port {}, server IP: {}..."
            .format(self.port, self.ip)
        )

        (self.client, self.addr) = self.socket.accept()
        print ("Connected! Connection address: ",self.addr)

    def _close_connection(self):
        if self.socket:
            self.socket.close()
            print ("Closed server socket")
        if self.client:
            self.client.close()
            print ("Closed client socket")

    def _send(self, bytes):
        return self.client.sendto(bytes, self.addr)

    def _recv(self):
        BUFF_SIZE = 1024
        data = b''
        while True:
            part = self.client.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data

if __name__ == "__main__":
    import time
    import os
    s = TCPServer("localhost", 50000)
    s.init_connection()
    while True:
        b = os.urandom(300)
        s.send(b)
        print("Server sent: {}".format(b))
        msg = s.recv()
        print("Server received: {}".format(msg))
        time.sleep(1)


