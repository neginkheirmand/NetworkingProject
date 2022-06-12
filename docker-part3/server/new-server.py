from http import client
import socket
import os, sys
from _thread import *
import json
import threading
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server


list_agents = []


socketData = {
    "static_agent": {
        "cpu_percent": "5",
        "ram_percent": "5"
        }
    }
    
class agentServer(object):

    def __init__(self):
        pass

    def collect(self):
        global socketData
        
        for key, value in socketData.items():
            index = key[0]+":"+str(key[1])
            g = GaugeMetricFamily("CPU_Usage", 'Help text', labels=['CPU_Usage'])
            g.add_metric([ index], value["cpu_percent"])
            yield g

            c = GaugeMetricFamily("RAM_Usage", 'Help text', labels=['RAM_Usage'])
            c.add_metric([ index ], value["ram_percent"])
            yield c

def create_metric():
    start_http_server(8000)
    REGISTRY.register(agentServer())



ServerSideSocket = socket.socket()
ThreadCount = 1

def create_socket():
    global ServerSideSocket, host, port, ThreadCount

    ServerSideSocket = socket.socket()
    host = '127.0.0.1'
    port = 2004
    ThreadCount = 1 #because of the static agent

def bind_socket():
    global ServerSideSocket, host, port
    
    try:
        ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
        print("closing the program since the port 2004 is in use")
        sys.exit(0)
    print('Succeded in binding the server to the port 2004, socket is listening...')
    ServerSideSocket.listen(5)

def end_connection(connection):
    connection.shutdown(socket.SHUT_RDWR)
    connection.close()

def print_data_agents():
    global ThreadCount, socketData, list_agents    
    print('Thread Number: ' + str(ThreadCount))
    print('list of agents as of right now:')
    for key, value in socketData.items():
        print("-----")
        if(key=="static_agent"):
            print(key)
            print("with data:")
            print(value)
            continue    
        print(key[0],":", str(key[1]))
        print("with data:")
        print(value)
        
    print('___________________________________')


def multi_threaded_client(connection, address):
    try:
        global ThreadCount, socketData, list_agents    
        connection.send(str.encode(str(address[1])))
        while True:
            data = connection.recv(2048)
            #the data is the dictionary as json 
            if not data:
                break
            agent_data_dict = json.loads(data.decode())
            socketData[address] = agent_data_dict
            connection.sendall(str.encode("alive"))
            print_data_agents()
        print("ending connection with agent:"+address[0]+str(address[1]))
        list_agents.remove((connection, address))
        del socketData[address]
        ThreadCount-=1
        end_connection(connection)
    except:
        list_agents.remove((connection, address))
        del socketData[address]
        ThreadCount-=1
        end_connection(connection)
        print("a connection with ", address[0], str(address[1]), "was forcibly closed by the remote host")
        print_data_agents()
        return
    
if __name__ == '__main__':
    create_metric()
    create_socket()
    bind_socket()
    try:
        while True:
            Client, address = ServerSideSocket.accept()

            print('Connected to: ' + address[0] + ':' + str(address[1]))

            start_new_thread(multi_threaded_client, (Client, address, ))
            ThreadCount += 1
            list_agents.append((Client, address))

        ServerSideSocket.close()
    except KeyboardInterrupt:
        print("keyboard interrupt")
        # print(str(e))
        print("ending")
        # ServerSideSocket.close()
        sys.exit(0)

