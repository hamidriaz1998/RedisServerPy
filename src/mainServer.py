import socket
from threading import Thread
from databaseHandler import Database
from commandExec import CommandExecutor
from redisParser import CommandParser


class Server:
    def __init__(self, address=("localhost", 6379)):
        self.server = socket.create_server(address)
        self.database = Database()
        self.executor = CommandExecutor(self.database)

    def handleClient(self, conn, addr):
        with conn:
            print(f"Connected to {addr}")
            while True:
                request = conn.recv(1024).decode()
                if not request:
                    print(f"Disconnected from {addr}")
                    break
                command, args = CommandParser.parse(request)
                response = self.executor.execute(command, args).encode()
                conn.sendall(response)

    def run(self):
        with self.server as server:
            server.listen()
            while True:
                conn, addr = server.accept()
                Thread(target=self.handleClient, args=(conn, addr)).start()
