import socket


def main():
    with socket.create_server(("localhost", 6379), reuse_port=True) as server:
        while True:
            server.listen()
            conn, addr = server.accept()
            with conn:
                print(f"Connected to {addr}")
                while True:
                    message = conn.recv(1024).decode()
                    if not message:
                        print("Disconnected")
                        break
                    print(f"Received this message: {message}")


if __name__ == "__main__":
    main()
