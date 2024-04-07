import json
from db_manager import DatabaseManager

class PurchasesManager:
    def __init__(self, items : dict) -> None:
        self.items = items

        self.db = DatabaseManager()
    def buy_item(self, message):
        status = 'fail'
        user = self.db.load_user(message['nickname'])
        if message['item'] in self.items.keys() and user['credits'] >= self.items[message['item']]:
            status = 'ok'

            new_credits_amout = user['credits'] - self.items[message['item']]
            self.db.update_credits(user['nickname'], new_credits_amout)

            new_resources = json.loads(user['resources'])
            new_resources.append(message['item'])

            self.db.update_resources(user['nickname'], new_resources)            
        else:
            status = 'fail'
        return {'status' : status}
    def sell_item(self, message):
        status = 'fail'
        user = self.db.load_user(message['nickname'])
        if message ['item'] in user['resources']:
            status = 'ok'

            new_credits_amout = user['credits'] + self.items[message['item']]
            self.db.update_credits(user['nickname'], new_credits_amout)

            new_resources = json.loads(user['resources'])
            new_resources.remove(message['item'])

            self.db.update_resources(user['nickname'], new_resources)

        return {'status' : status}
    
