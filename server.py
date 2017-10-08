import os
import socket
import sys
from logging import *
from threading import Thread, current_thread
import threading

# TODO: zrobic strukture client = {socket: _, ip: _, port: _} i przesylac ja (jako kwargs?) zamiast 3 argumentow
basicConfig(filename='logs/server.log', format='[%(asctime)s]: %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S',
            level=DEBUG)


def log(msg, level):
    level(msg)


log("Starting " + os.path.basename(sys.argv[0]), info)


class Server:
    socket = None
    address = 'localhost'
    port = 10001
    timeout = None
    clients = []
    threads = []

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log("Initialized server socket.", info)
        self.socket.bind((self.address, self.port))
        log("Binded server socket to " + self.address + ":" + str(self.port) + ".", info)
        self.socket.settimeout(self.timeout)
        log("Set server socket timeout to " + str(self.timeout) + ".", info)
        self.start_thread("listen_thread")

    def listen_thread(self):
        self.socket.listen()
        while True:
            self.accept_connection()
            self.clear_threads()

    def client_thread(self, **kwargs):
        client_socket = kwargs["socket"]
        client_ip = kwargs["ip"]
        client_port = kwargs["port"]
        try:
            data = b''
            while True:
                data += client_socket.recv(2048)
                if data == b'':
                    log("Connection with socket " + client_ip + " is broken.", error)
                    self.end_connection(socket=client_socket, ip=client_ip)
                elif data == b'q;':
                    self.end_connection(socket=client_socket, ip=client_ip)
                    break
                elif data.endswith(b';'):
                    if data == b'offline;':
                        # ustaw status offline
                        pass
                    elif data == b'online;':
                        # ustaw status online
                        pass
                    elif data == b'accept;':
                        # akceptuj wizytę
                        pass
                    elif data == b'reject;':
                        # odrzuć wizytę
                        pass
                    else:
                        print(bytes.decode(data, "utf-8"))
                    data = b''

        except ConnectionResetError:
            log("Connection with client " + client_ip + " was closed by remote host.", error)

    def start_thread(self, name, **kwargs):
        thread = Thread(name=name, target=getattr(self, name, self.client_thread), kwargs=kwargs)
        thread.start()
        log("Started new thread: " + name, info)
        self.threads.append(thread)

    def accept_connection(self):
        client_socket, client_address = self.socket.accept()
        log("Accepted connection from " + client_address[0] + ":" + str(client_address[1]) + ".", info)
        client = {"socket": client_socket, "ip": client_address[0], "port": client_address[1]}
        self.clients.append(client)
        self.start_thread("client_thread", socket=client_socket, ip=client_address[0], port=client_address[1])

    def end_connection(self, **kwargs):
        client_socket = kwargs["socket"]
        client_ip = kwargs["ip"]
        log("Closing the connection with client " + client_ip + ".", info)
        client_socket.shutdown(0)
        client_socket.close()
        log("Connection with client " + client_ip + " is closed.", info)
        self.clients.remove([client for client in self.clients if client["socket"] == client_socket][0])
        self.clear_threads()

    def clear_threads(self):
        for thread in self.threads:
            if not thread.is_alive():
                self.threads.remove(thread)
        print(self.threads)

    def close_socket(self):
        self.socket.shutdown()
        self.socket.close()


server = Server()
