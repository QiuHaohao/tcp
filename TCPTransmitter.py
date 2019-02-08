import sys

class TCPTransmitter(object):
    def __init__(self, ip="localhost", port=50000):
        self.ip = ip
        self.port = port
        self.is_connected = False
        self.buffer = ''

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

    def send(self, message):
        try:
            self._send(message)
        except Exception as e:
            print ("\nPC Write Error: %s " % str(e))
            self.reset_connection()

    def recv(self):
        try:
            while not '\n' in self.buffer:
                self.buffer += self._recv()
            if '\r\n' in self.buffer:
                line, self.buffer = self.buffer.split('\r\n', 1)
            else:
                line, self.buffer = self.buffer.split('\n', 1)
            return line
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print ("\nPC Read Error: %s " % str(e))
            self.reset_connection()