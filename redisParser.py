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
