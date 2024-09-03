import socket

def get_username():
    """ Prompt the client to enter their username. """
    return input("Enter your client username: ")

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

# Initialize the game board and socket
table_client = [[" " for _ in range(3)] for _ in range(3)]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
port = 15000  
serverAddr = ('10.119.76.103', port)

# Get the client username and communicate with server
username = get_username()  # Get the client username
print(f"{username} has joined the game.\n")
s.sendto(username.encode(), serverAddr)
data, addr = s.recvfrom(1024)
server_username = data.decode()

# Initialize player symbols
client_symbol = input("Pick your symbol (X/O): ")
s.sendto(client_symbol.encode(), serverAddr)
print(f"Sent symbol '{client_symbol}' to server.\n")
server_symbol = 'O' if client_symbol == 'X' else 'X'

# Wait for the server to acknowledge
ack, addr = s.recvfrom(1024)
print("Received from server:", ack.decode())

# Determine who goes first
first_turn, addr = s.recvfrom(1024)
first_turn = first_turn.decode()
print(f"\nReceived first turn decision: {first_turn}")

# Confirm receipt of who goes first
confirmation = f"{first_turn} will go first"
s.sendto(confirmation.encode(), serverAddr)
print(f"Sent confirmation to server: {confirmation}")

winner = None

# Client main game loop
try:
    client_starts = (first_turn == username)

    while True:
        if not client_starts:
            # Wait for server's move before making a move if the server goes first
            print(f"\nWaiting for {server_username} to make a move...")
            data, addr = s.recvfrom(1024)
            message = data.decode()

            # Immediately handle game-ending messages
            if "wins" in message or "Draw." in message:
                if "wins" in message:
                    winner = message.split()[0]
                else:
                    winner = "Draw"
                break


            move = tuple(map(int, message.split(',')))
            if make_move(table_client, move, server_symbol):
                print_board(table_client, server_username)

                # Check for a win or draw after processing the move
                if check_win(table_client, server_symbol):
                    winner = server_username  # Save the server's username as the winner
                    break
                elif check_draw(table_client):
                    winner = "Draw"  # Save 'Draw' if the game ends in a draw
                    break

            client_starts = True

        if client_starts:
            print(f"\n{username}'s turn to move.")
            print_board(table_client, username)
            move = get_move()
            if make_move(table_client, move, client_symbol):
                s.sendto(f"{move[0]},{move[1]}".encode(), serverAddr)
                # Check for a win or draw after the client's move
                if check_win(table_client, client_symbol):
                    winner = username  # Save the client's username as the winner
                    break
                elif check_draw(table_client):
                    winner = "Draw"  # Save 'Draw' if the game ends in a draw
                    break
                
                client_starts = False 

            else:
                print("That space is taken. Try again.")
                continue

except socket.timeout:
    print("Server response timed out.")
finally:
    if winner:
        print(f"\n{winner} is the winner!") if winner != "Draw" else print("\nThe game is a draw.")
    s.close()
    print("Client socket closed.")