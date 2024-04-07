import socket
import json
from actions.items_loader import ItemsLoader
from actions.account_updater import AccountDataUpdater
from actions.purchases_manager import PurchasesManager
from db_manager import DatabaseManager

class ServerManager:
    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 9999)  
        self.actions = {}
        self.db_manager = None

    def server_controller(self):
        self.start_server()

        while True:
            connection, clientAddress = self.server_socket.accept()
            print("Connection from: {}".format(clientAddress))
            try:
                while True:
                    data = connection.recv(1024)
                    if data:
                        message = json.loads(data.decode())

                        response = None

                        print("Recieved from client: {}".format(message))
                        if message['type'] == 'command':
                            action = self.actions[message['command'].lower()]
                            if message['command'] == 'items':
                                response = action()
                            else:
                                response = action(message)
                        elif message['type'] == 'login':
                            response = self.user_login(message['nickname'])               
                        else:
                            print("Unknow action: ".format(message))
        
                        
                        response = json.dumps(response)
                        print("Sent to client: {}".format(response))
                        connection.sendall(response.encode())

                    else:
                        break
            finally:
                connection.close()


    def user_login(self, nickname):
        dataLoader = AccountDataUpdater()
        if self.db_manager.load_user(nickname) != None:
            return {"new_account" : 0, "account_data" : dataLoader.update_on_login(nickname)}
        else:
            self.db_manager.create_user(nickname)
            return {"new_account" : 1, "account_data" : dataLoader.update_on_login(nickname)}
        
    

    def start_server(self):
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(1)  

        self.setup_actions()

        self.db_manager = DatabaseManager()
        self.db_manager.init_database()
        print("Server started, waitig for client...")  

    def setup_actions(self):
        self.actions['items'] = ItemsLoader.load_items
        
        dataLoader = AccountDataUpdater()
        self.actions['refresh'] = dataLoader.update_on_purchase

        pm = PurchasesManager(ItemsLoader.load_items())
        self.actions['sell'] = pm.sell_item
        self.actions['buy'] = pm.buy_item

if __name__ == "__main__":
    serverManager = ServerManager()
    serverManager.server_controller()
