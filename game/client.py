import os
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock



class Client:
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    ADDR = (HOST, PORT)
    
    def __init__(self, name="Player"):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self, data):
        pass

    def receive(self):
        pass
