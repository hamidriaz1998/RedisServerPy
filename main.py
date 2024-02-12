import socket
import threading


class Database:
    def __init__(self):
        self.DB = {}

    def set(self, key, value):
        self.DB[key] = value

    def get(self, key):
        return self.DB.get(key)

    def delete(self, key):
        if key in self.DB:
            del self.DB[key]


class CommandParser:
    @staticmethod
    def parse(request):
        if request.startswith("*"):
            parts = request.split("\r\n")
            command = parts[2].upper()
            args = parts[4:-1:2]
            return command, args
        else:
            raise ValueError("Invalid command format")


class CommandExecutor:
    def __init__(self, database):
        self.db = database

    def __echo(self, args):
        return "+" + " ".join(args) + "\r\n"

    def __ping(self, args):
        if not args:
            return "+PONG\r\n"
        else:
            return "+" + " ".join(args) + "\r\n"

    def __set(self, args):
        try:
            self.db.set(args[0], args[1])
            if len(args) == 4:
                threading.Timer(
                    int(args[3]) / 1000, function=self.db.delete, args=(args[0],)
                ).start()
            return "+OK\r\n"
        except:
            return "-ERR wrong number of arguments for 'set' command\r\n"

    def __get(self, args):
        try:
            value = self.db.get(args[0])
            if value:
                return f"${len(value)}\r\n{value}\r\n"
            else:
                return "$-1\r\n"
        except:
            return "-ERR wrong number of arguments for 'get' command\r\n"

    def execute(self, command, args):
        if command == "ECHO":
            return self.__echo(args)
        elif command == "PING":
            return self.__ping(args)
        elif command == "SET":
            return self.__set(args)
        elif command == "GET":
            return self.__get(args)


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
                threading.Thread(target=self.handleClient, args=(conn, addr)).start()


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
