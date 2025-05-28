import socket
import threading

HOST = '127.0.0.1'  # Localhost
PORT = 5555         # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

def receive_connections():
    print("Server is running...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        clients.append(client)
        client.send("Welcome to the MCP-style server!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
