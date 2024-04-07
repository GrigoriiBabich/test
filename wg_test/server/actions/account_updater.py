import config
from db_manager import DatabaseManager

class AccountDataUpdater:
    def update_on_login(self, nickname) -> dict:
        db = DatabaseManager()
        new_credits_amout = self.account_data_request(nickname)['credits'] + config.credits_on_login
        db.update_credits(nickname, new_credits_amout)

        return self.account_data_request(nickname)
    
    def update_on_purchase(self, message):
        return self.account_data_request(message['nickname'])
        
    def account_data_request(self, nickname):
        db = DatabaseManager()
        return db.load_user(nickname)

    
