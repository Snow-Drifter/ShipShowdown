import socket

HOST = '127.0.0.1'  # localhost
PORT = 8888         # arbitrary port


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        while True:
            # Receive message from the server
            data = client_socket.recv(1024)
            if data == b'':
                print("Disconnected")
                break
            
            needs_reply = handle_response(data.decode())
            if needs_reply:
                try:
                    message = input("Input: ")
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

    print("Connection closed.")


def handle_response(message) -> bool:
    # returns True if it expects a response from the player
    match message.split(":"):
        case ["notice", "turn_start"]:
            print("Your turn.")
            return True
        case ["notice", "enemy_move", move]:
            print(f"Enemy moved. {move}")
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
    return False

try:
    start_client()
# handle ctrl + c gracefully
except KeyboardInterrupt:
    print("Shutting down...")
