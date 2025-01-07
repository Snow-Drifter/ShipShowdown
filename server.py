import socket


class Player:
    def __init__(self, connection):
        self.socket, self.address = connection

    def notify_start_turn(self):
        self.socket.send("notice:turn_start".encode())
        
    def notify(self, notice):
        self.socket.send(f"notice:{notice}".encode())
    
    def receive_message(self):
        return self.socket.recv(255).decode()
    
    def take_turn(self):
        self.notify_start_turn()
        return self.receive_message()
    
    def kick(self):
        self.socket.send(f"kicked".encode())


def main():
    # Server code to accept two clients and alternate turns
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(2)

    print("Waiting for players...")

    player1 = Player(server_socket.accept())
    print("Player 1 connected.")

    player2 = Player(server_socket.accept())
    print("Player 2 connected.")

    while True:
        move = player1.take_turn()
        if move == '':
            print("Player 1 disconnected")
            player2.kick()
            break
        print(f"Received '{move}' from player 1.")
        player2.notify(f"enemy_move:{move}")
        
        move = player2.take_turn()
        if move == '':
            print("Player 2 disconnected")
            player1.kick()
            break
        print(f"Received '{move}' from player 2.")
        player1.notify(f"enemy_move:{move}")


try:
    main()
except KeyboardInterrupt:
    print("Shutting down...")
