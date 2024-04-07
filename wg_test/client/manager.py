import socket
import json
import sys
from config import hostname, port
from states import ClientStates
from session_data import SessionData
from commands import Commands


class ClientManager:
    def __init__(self) -> None:
        self.clientState = ClientStates.NONE
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = None
        self.session_data = None
        
    def run_client(self):
        self.connect_to_server()

        self.clientState = ClientStates.LOGIN
        self.commands = Commands().commands_list

        while True:
            if self.clientState == ClientStates.LOGIN:
                user_message = input("Enter nickname. If you want to close client, enter exit: ")
                if user_message.lower() == 'exit':
                    self.clientSocket.close()
                    sys.exit()
                self.user_login(user_message)

            elif self.clientState == ClientStates.GAME_SESSION:
                user_message = input(": ")
                self.process_command(user_message)
    def connect_to_server(self):
        serverAddress = (hostname, port)
        try:
            self.clientSocket.connect(serverAddress)
            print("Server connection successfull")
            return True
        except socket.error:
            print("Server unavaliable. Please, start server")
            return False

    def process_command(self, user_message):
        user_message = user_message.split(' ', 2)
        
        if user_message[0].lower() in self.commands:
            command = self.commands[user_message[0].lower()]
            if len(user_message) == 1 and (user_message[0] != 'sell' and user_message[0] != 'buy'):
                command(self.session_data)
            elif len(user_message) > 1 and (user_message[0] == 'sell' or user_message[0] == 'buy'):
                command(self.clientSocket, self.session_data, user_message[1])
            else:
                print("Command not found")
        elif user_message[0].lower() == 'exit':
            self.clientSocket.close()
            sys.exit()
        elif user_message[0].lower() == 'logout':
            self.user_logout()
        else:
            print("Command not found")


    def user_login(self, nickname):
        message = {'type': 'login', "nickname": nickname}
        self.clientSocket.send(json.dumps(message).encode())

        response = json.loads(self.clientSocket.recv(1024).decode())

        self.session_data = SessionData(response['account_data'], self.clientSocket)
        if response["new_account"] == 0:
            print("Login with account {} successefull".format(self.session_data.user_data['nickname']))
        else:
            print("Account {} created, login succesessfull".format(self.session_data.user_data['nickname']))

        self.clientState = ClientStates.GAME_SESSION

    def user_logout(self):
        self.clientState = ClientStates.LOGIN
        print('User {} logout'.format(self.session_data.user_data['nickname']))
        self.session_data = None

if __name__ == "__main__":
    clientManager = ClientManager()
    clientManager.run_client()
