# echo-client.py

from codecs import namereplace_errors
import socket
import json
import psutil
import time
import sys

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



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def end():
    global s
    try:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    except:
        return

def create_agent():
    HOST = "0.0.0.0"  # The server's hostname or IP address
    PORT = 2004  # The port used by the server
    try:
        global s
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            port_number = s.recv(1024).decode()
            print("agent on port", port_number, "started, connection to the server stablished")
            time.sleep(1)
            while(True):
                a = str(getData())
                time.sleep(1)
                s.sendall(bytes(bytearray(a, encoding='utf-8')))
                data = s.recv(1024)
                if not data:
                    end()
                    # exit()
                    return
    except KeyboardInterrupt:
        print("keyboard interrupt detected, exiting...")
        end()
        sys.exit(0)
    except:
        end()
        return


if __name__ == '__main__':
    try:
        while(True):
            create_agent()
            end()
    except KeyboardInterrupt:
        print("keyboard interrupt detected, exiting...")
        end()
        sys.exit(0)