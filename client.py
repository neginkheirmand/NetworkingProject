# echo-client.py

from codecs import namereplace_errors
import socket
import json
import psutil
  


def getCpuPercentage(time):
    # print('The CPU usage is: ', psutil.cpu_percent(4))
    return psutil.cpu_percent(time)

def getRamPercentage():
    return psutil.virtual_memory()[2]

def getData():
    data = {
    "cpu_percent": getCpuPercentage(1),
    "ram_percent": getRamPercentage()
    }
    data = json.dumps(data)
    return data



HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # a = input("client: ")
    a = "cpu spec "+ str(getData())
    s.sendall(bytes(bytearray(a, encoding='utf-8')))
    data = s.recv(1024)

print(f"Received {data!r}")