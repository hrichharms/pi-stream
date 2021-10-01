# pi-stream
Python scripts to stream camera data from raspberry pi to display server.


## Usage

Server:

```python3 SERVER/server.py <host port>```

Client:

```python3 CLIENT/client.py <server ip> <server_port>```


## Configuration

All configuration options not in the usage arguments are in constants in the respective program's code. At the moment, only the client script has such configuration options, including: client bind port, camera resolution, and camera fps.
