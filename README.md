# Networked Tic-Tac-Toe Game

This project consists of a simple networked Tic-Tac-Toe game implemented in Python. The game uses UDP (User Datagram Protocol) for communication between a server and a client. The server hosts the game, while the client connects to it to play.

## Files

- **udpserver.py**: This script runs the server side of the game. The server is responsible for managing the game state, validating moves, and communicating the game board status to the client.
- **udpclient.py**: This script runs the client side of the game. The client sends the player's moves to the server and receives updates on the game state.

## Features

- **Network Communication**: Uses UDP for fast, connectionless communication between the server and the client.
- **Interactive Gameplay**: The game allows two players to play Tic-Tac-Toe remotely, with the server maintaining the game board and game logic.
- **User Input Validation**: Both the server and client scripts include input validation to ensure that the players' moves are within the bounds of the game board.

## How to Run

1. **Start the Server**:
   - Run the `udpserver.py` script on a machine that will act as the game server.
   - The server will prompt for the username and wait for the client to connect.

   ```bash
   python udpserver.py

2. **Connect as a Client**:
   - Run the udp_client.py script on a different machine or the same machine, depending on your setup.
   - The client will prompt for the username and the server's IP address to connect.

   ```bash
   python udp_client.py

3. **Gameplay**:
   - The game board is displayed after each move, and players are prompted to enter their move coordinates (row and column).
   - The game continues until one player wins or the board is full.
  
4. **Requirements**:
   - Python 3.x
   - Both server and client should be on the same network or connected over the internet (adjust firewalls and NAT settings as necessary).

5. **Notes**:
   - The game currently supports a 3x3 Tic-Tac-Toe board.
   - The server and client scripts are designed to work together; running multiple clients against the same server is not supported in this version.
   - UDP is a connectionless protocol, which may result in lost packets in unreliable networks. Ensure that your network is stable for the best experience.
