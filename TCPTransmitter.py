import sys

class TCPTransmitter(object):
    def __init__(self, ip="192.168.5.5", port=50000):
        self.ip = ip
        self.port = port
        self.is_connected = False
        self.buffer = []

    def is_connected(self):
        return self.is_connected

    def init_connection(self):
        try:
            self._setup_connection()
            self.is_connected = True
        except KeyboardInterrupt:
            sys.exit()
            print ("Connection closed")
        except Exception as e:
            print ("\nError: %s" % str(e))

    def close_connection(self):
        self._close_connection()
        self.is_connected = False

    def reset_connection(self):
        self.close_connection()
        self.init_connection()

    def send(self, bytes):
        try:
            self._send(bytes)
        except Exception as e:
            print ("\nPC Write Error: %s " % str(e))
            self.reset_connection()

    def recv(self):
        try:
            bytes_recved = self._recv()
            print(bytes_recved)
            return bytes_recved
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print ("\nPC Read Error: %s " % str(e))
            self.reset_connection()

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data