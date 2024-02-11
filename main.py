import socket
import threading


def handleClient(conn: socket, addr):
    with conn:
        print(f"Connected to {addr}")
        while True:
            message = conn.recv(1024).decode()
            if not message:
                print(f"Disconnected from {addr}")
                break
            print(f"Received a message from {addr}: {message}")


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
