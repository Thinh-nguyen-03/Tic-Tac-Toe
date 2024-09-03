import random
import socket

def get_username():
    """ Prompt the user to enter the server username. """
    return input("Enter your server username: ")

def print_board(board, username):
    """ Display the game board with the current player's username indicated. """
    print(f"\n{username}'s move:")
    for row in board:
        print("|" + "|".join(f"{cell:^3}" for cell in row) + "|")
        print("-------------")

def make_move(board, move, symbol):
    """ Place a symbol on the board at the specified coordinates if the cell is empty. """
    x, y = move
    if board[x][y] == ' ':
        board[x][y] = symbol
        return True
    return False

def get_move():
    """ Prompt the player to enter their move coordinates and validate the input. """
    while True:
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter col (1-3): ")) - 1
            if 0 <= row <= 2 and 0 <= col <= 2:
                return row, col
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Please enter numbers only.")

def check_win(board, symbol):
    """ Check all win conditions for the specified symbol. """
    for row in board:
        if all(s == symbol for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False   

def check_draw(board):
    """ Check if the board is full and no moves are left. """
    return all(cell != ' ' for row in board for cell in row)

# Server setup
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "10.229.21.142"
port = 15000
serversocket.bind((ip, port))

username = get_username()
print(f"{username} has started the server\n")

# Exchange usernames with the client
data, addr = serversocket.recvfrom(1024)
client_username = data.decode()
serversocket.sendto(username.encode(), addr)

# Handle initial game setup
data, addr = serversocket.recvfrom(1024)
client_symbol = data.decode()
server_symbol = 'O' if client_symbol == 'X' else 'X'
ack_message = f"{username} will be '{server_symbol}'"
serversocket.sendto(ack_message.encode(), addr)
print(f"Sent acknowledgment to client: {ack_message}\n")

# Decide and announce who goes first
first_turn = client_username
serversocket.sendto(first_turn.encode(), addr)
print(f"Decided first turn: {first_turn}\n")

# Receive client's game-start confirmation
data, addr = serversocket.recvfrom(1024)
print(f"Received confirmation from client: {data.decode()}\n")

table_server = [[" " for _ in range(3)] for _ in range(3)]

winner = None

# Server main game loop
try:
    # If the server goes first, make the first move
    if first_turn == username:
        print(f"{username}'s turn to make the first move.")
        print_board(table_server, username)
        move = get_move()
        if make_move(table_server, move, server_symbol):
            serversocket.sendto(f"{move[0]},{move[1]}".encode(), addr)

    while True:
        # Handle client's move
        print(f"\nWaiting for {client_username}'s response...")
        data, addr = serversocket.recvfrom(1024)
        move = tuple(map(int, data.decode().split(',')))

        if make_move(table_server, move, client_symbol):
            print_board(table_server, client_username)

            if check_win(table_server, client_symbol):
                serversocket.sendto(f"{client_username} wins!".encode(), addr)
                winner = client_username
                break
            elif check_draw(table_server):
                serversocket.sendto("Draw.".encode(), addr)
                print("The game is a draw.")
                break

            # Process server's next move
            print(f"\n{username}'s turn to move.")
            print_board(table_server, username)
            move = get_move()
            if make_move(table_server, move, server_symbol):
                serversocket.sendto(f"{move[0]},{move[1]}".encode(), addr)
                print_board(table_server, username)
               
                # Check if the server's move resulted in a win
                if check_win(table_server, server_symbol):
                    winner = username
                    serversocket.sendto(f"{username} wins!".encode(), addr)
                    break

                # Check if the game is a draw after the server's move
                elif check_draw(table_server):
                    winner = "Draw"
                    serversocket.sendto("Draw.".encode(), addr)
                    break

            else:
                print("That space is taken. Try again.")
                continue
        else:
            print(f"Invalid move from {client_username}.")

except socket.timeout:
    print("No response from the client. Game over.")
finally:
    # Announce the game outcome before closing
    if winner:
        print(f"\n{winner} is the winner!") if winner != "Draw" else print("\nThe game is a draw.")
    serversocket.close()
    print("Server socket closed.")