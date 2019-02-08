import socket
from TCPTransmitter import TCPTransmitter

class TCPClient(TCPTransmitter):
    def __init__(self, *args):
        super(TCPClient, self).__init__(*args)
        self.socket = None

    def _setup_connection(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print ("Trying to connect to rpi")
        self.socket.connect((self.ip, self.port))
        print ("Connected! Connection address: ",self.socket)

    def _close_connection(self):
        if self.socket:
            self.socket.close()
            print ("Closed client socket")

    def _send(self, s):
        return self.socket.send(str(s+'\n').encode('UTF-8'))

    def _recv(self):
    	return self.socket.recv(1024).decode('utf-8')

if __name__ == "__main__":
    import time
    c = TCPClient("localhost", 50000)
    c.init_connection()
    n = 0
    while n < 5000:
        c.send(str(n))
        n += 1
        msg = c.recv()
        print("Received: {}".format(msg))
        time.sleep(1)