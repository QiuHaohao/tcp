# tcp
TCP server and client created for communication between Rpi and PC over Wi-Fi in MDP


## Usage
The module includes two classes: `TCPServer` and `TCPClient`. Both classes provides the same set of methods (`send`, `recv`, `init_connection`, `reset_connection` and `is_connected`) . The only difference is that the `TCPServer` should start listen by calling `init_connection` for incoming connection first before `TCPClient` attempts to `init_connection`. `TCPServer` connects with the first incoming connection it listens. Once the connection is established, string messages can be sent and received between the `TCPServer` and `TCPClient`.

In MDP, the rpi should be using `TCPServer` and the PC should be using `TCPClient`.

The follows is an example of using this module from a script under the folder containing this module:

```
### on server 

src/
    server.py
    tcp
```
```python
# server.py

import time
from tcp import TCPServer

IP_SERVER = "192.168.5.5"
PORT_SERVER = 50000

s = TCPServer(IP_SERVER, PORT_SERVER)
s.init_connection()
n = 0
while n < 5:
    s.send(str(n))
    n += 1
    msg = s.recv()
    print("Server Received: {}".format(msg))
    time.sleep(1)
```

```
### on client 

src/
    client.py
    tcp
```

```python
# client.py

import time
from tcp import TCPClient

IP_SERVER = "192.168.5.5"
PORT_SERVER = 50000

c = TCPClient(IP_SERVER, PORT_SERVER)
c.init_connection()
n = 0
while n < 5:
    c.send(str(n))
    n += 1
    msg = c.recv()
    print("Client Received: {}".format(msg))
    time.sleep(1)
```

Run the script on the server first, then on the client.
```bash
# on server @ 192.168.5.5
python server.py 
# Listening for incoming connections...
# Connected! Connection address:  ('192.168.5.6', 59777)
# Server Received: 0
# Server Received: 1
# Server Received: 2
# Server Received: 3
# Server Received: 4
```

```bash
# on client @ 192.168.5.6
python client.py 
# Trying to connect to server
# Connected! Connection address:  <socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.5.6', 59777), raddr=('192.168.5.5', 50000)>
# Client Received: 0
# Client Received: 1
# Client Received: 2
# Client Received: 3
# Client Received: 4
```
