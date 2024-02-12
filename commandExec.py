from threading import Timer


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
                Timer(
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
