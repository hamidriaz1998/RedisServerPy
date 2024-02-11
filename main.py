import socket
import threading


def parseRequest(request: str):
    """
    Parse the request string and extract the command and its arguments.

    Args:
        request (str): The request string.

    Returns:
        Tuple[str, list[str]]: A tuple containing the command and its arguments.
    """
    if request.startswith("*"):  # Bulk arrays
        parts = request.split("\r\n")
        command = parts[2].upper()
        args = parts[4:-1:2]
        return command, args
    else:
        raise ValueError("Invalid command format")


def generateResponse(command: str, args: list[str]):
    """
    Generate the response string based on the command and its arguments.

    Args:
        command (str): The command.
        args (list[str]): The arguments.

    Returns:
        str: The response string.
    """
    if command == "ECHO" or (command == "PING" and args):
        return "+" + " ".join(args) + "\r\n"
    elif command == "PING" and not args:
        return "+PONG\r\n"
    else:
        raise ValueError("Unsupported command")


def handleClient(conn: socket, addr):
    with conn:
        print(f"Connected to {addr}")
        while True:
            request = conn.recv(1024).decode()
            if not request:
                print(f"Disconnected from {addr}")
                break
            command, args = parseRequest(request)
            response = generateResponse(command, args).encode()
            conn.sendall(response)


def main():
    with socket.create_server(("localhost", 6379), reuse_port=True) as server:
        server.listen()
        while True:
            try:
                conn, addr = server.accept()
            except Exception as e:
                print(f"Error occured: {e}")
            clientThread = threading.Thread(
                target=handleClient, args=(conn, addr), daemon=True
            )
            clientThread.start()


if __name__ == "__main__":
    main()
