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
        print ("Listening for incoming connections...")

        (self.client, self.addr) = self.socket.accept()
        print ("Connected! Connection address: ",self.addr)

    def _close_connection(self):
        if self.socket:
            self.socket.close()
            print ("Closed server socket")
        if self.client:
            self.client.close()
            print ("Closed client socket")

    def _send(self, s):
        return self.client.sendto(str(s+'\n').encode('UTF-8'), self.addr)

    def _recv(self):
        return self.client.recv(1024).decode('utf-8')

if __name__ == "__main__":
    import time
    s = TCPServer("localhost", 50000)
    s.init_connection()
    n = 0
    while n < 5000:
        s.send(str(n))
        n += 1
        msg = s.recv()
        print("Received: {}".format(msg))
        time.sleep(1)


