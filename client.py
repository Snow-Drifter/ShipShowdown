import socket

HOST = '127.0.0.1'  # localhost
PORT = 8888         # arbitrary port


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        while True:
            try:
                message = input("Enter your message (type 'exit' to quit): ")
            except EOFError:
                print("InputError")
                continue
            
            if message == "":
                print("Message Empty. Not Sent.")
                continue

            if message.lower() == 'exit':
                print("Closing the connection...")
                break
            # Send the message to the server
            client_socket.sendall(message.encode())

            # Receive the response from the server
            data = client_socket.recv(1024)

            handle_response(data.decode())

    print("Connection closed.")


def handle_response(message):
    match message.split(":"):
        case ["kicked"]:
            # handle server kicking player
            print("Server kicked you!")
        case ["goodbye"]:
            # handle server kicking player
            print("You have left the server.")
        case ["invalid"]:
            # handle invalid request
            print("Server could not process your request.")
        case ["result", result]:
            print(f"Your action resulted in: '{result}'.")
        case ["message", message]:
            # todo handle messages containing colons
            print(f"Server: '{message}'.")
        case _:
            print("Received malformed response.")


try:
    start_client()
# handle ctrl + c gracefully
except KeyboardInterrupt:
    print("Shutting down...")
