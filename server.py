# agent-server.py

import socket
import json
import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import sys

socketData = {
    "cpu_percent": "5",
    "ram_percent": "5"
    }
class agentServer(object):

    def __init__(self):
        pass

    def collect(self):
        global socketData
        g = GaugeMetricFamily("MemoryUsage", 'Help text', labels=['Memory used Percentage: '])
        g.add_metric(["cpu percent"], socketData['cpu_percent'])
        yield g

        c = GaugeMetricFamily("RamUsage", 'Help text', labels=['RAM used Percentage: '])
        c.add_metric(["ram percent"], socketData['ram_percent'])
        yield c
        
        # print(socketData['cpu_percent'])
        # print(socketData['ram_percent'])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def end():
    global s
    global conn
    try:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    except:
        return

def Create_agent_server():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server
    global socketData
    try:
        start_http_server(8000)
        REGISTRY.register(agentServer())
        print(1)
        global s
        global conn
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(1.5)
            s.bind((HOST, PORT))
            print(1.5)
            s.listen()

            conn, addr = s.accept()
            print(2)
            with conn:
                print(f"Connected by {addr}")
                while True:
                    print(3)
                    data = conn.recv(1024)
                    if not data:
                        end()
                        break
                    socketData = json.loads(data.decode())
                    print("received" , str(data.decode()))
                    conn.sendall(data)
                print("done")
            print("done2")
        print("done 3")
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
            print(1)
            time.sleep(1)
            Create_agent_server()
            end()

    except KeyboardInterrupt:
        print("keyboard interrupt detected, exiting...")
        end()
        sys.exit(0)

# print(socketData)