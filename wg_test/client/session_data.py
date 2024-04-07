import json
import socket

class SessionData:
    def __init__(self, user_data, client_socket: socket.socket) -> None:
        self.client_socket = client_socket
        self.user_data = user_data
        self.server_items = self.load_server_items()

    def refresh_user_data(self):
        message = {'type': 'command', 'command': 'refresh', "nickname": self.user_data['nickname']}
        self.client_socket.sendall(json.dumps(message).encode())
        self.user_data = json.loads(self.client_socket.recv(1024).decode())

    def load_server_items(self) -> dict:
        command = {'type': 'command', 'command': 'items'}
        self.client_socket.send(json.dumps(command).encode())
        return json.loads(self.client_socket.recv(1024).decode())
