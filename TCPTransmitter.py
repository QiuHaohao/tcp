import queue
import sys
from .DataPaunp import DataPaunp

class TCPTransmitter(object):
    def __init__(self, ip="192.168.5.5", port=50000):
        self.ip = ip
        self.port = port
        self.is_connected = False
        self.buffer = queue.Queue()
        self.dpu = DataPaunp()

    def is_connected(self):
        return self.is_connected

    def init_connection(self):
        try:
            self._setup_connection()
            self.is_connected = True
        except KeyboardInterrupt:
            print ("Connection closed")
            self.close_connection()
            sys.exit()
        except Exception as e:
            print ("\nError: %s" % str(e))
            self.close_connection()

    def close_connection(self):
        self._close_connection()
        self.is_connected = False

    def reset_connection(self):
        self.close_connection()
        self.init_connection()

    def send(self, bytes):
        try:
            bytes_packed = self.dpu.pack(bytes)
            self._send(bytes_packed)
        except Exception as e:
            print ("\nPC Write Error: %s " % str(e))
            self.reset_connection()

    def recv(self):
        if self.buffer.empty():
            bytes_recved = self._recv_and_buffer()
            msgs_recved = self.dpu.unpack(bytes_recved)
            for msg in msgs_recved:
                self.buffer.put(msg)
        return self.buffer.get()

    def _recv_and_buffer(self):
        try:
            bytes_recved = self._recv()
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