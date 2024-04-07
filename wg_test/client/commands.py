import socket
import json
from tabulate import tabulate
from session_data import SessionData

class Commands:
    def __init__(self) -> None:        
        self.commands_list = {
            'items' : self.game_items,
            'my_items' : self.my_items,
            'credits' : self.credits,
            'buy' : self.buy_item,
            'sell' : self.sell_item
        }

    def my_items(user_data, session_data): 
        user_data = session_data.user_data
        resources = json.loads(user_data['resources']) if user_data['resources'] else ''
        
        f_data = {'Nickname' : user_data['nickname'], 
                  'Credits' : user_data['credits'], 
                  'Resources' : resources}
        
        print(tabulate(f_data.items()))  
        
    def credits(self, session_data):
        print('Credits: {}'.format(session_data.user_data['credits']))

    def game_items(self, session_data):
        print(tabulate(session_data.server_items.items(), headers=["Name", "Price"]))

    def buy_item(self, client_socket, session_data, item = None):
        self.transaction(client_socket, session_data, 'buy', item)

    def sell_item(self, client_socket, session_data, item = None):
        self.transaction(client_socket, session_data, 'sell', item)

    def transaction(self, client_socket, session_data : SessionData, command_type, item=None):
        command = {'type': 'command', 'command': command_type, 'item': item, 'nickname': session_data.user_data['nickname']}
        client_socket.send(json.dumps(command).encode())
        response = json.loads(client_socket.recv(1024).decode())

        if response['status'] == 'ok':
            print('Item {} successfully {}'.format(item, 'purchased' if command_type == 'buy' else 'sold'))
        else:
            print('Purchase unsuccessful, try again' if command_type == 'buy' else 'You do not have that item')
        session_data.refresh_user_data()