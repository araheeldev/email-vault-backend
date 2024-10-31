from rococo.data import MySqlAdapter
from rococo.repositories import BaseRepository
from common.models.user import User

class UserRepository(BaseRepository):
    def __init__(self, adapter: MySqlAdapter, message_adapter):
        super().__init__(adapter, User, message_adapter)
    
    def find_by_email(self, email):
        return self.get_one({'email': email})

    def find_by_referral_code(self, referral_code):
        return self.get_one({'referral_code': referral_code})
    
    def save_user(self, user):
        self.save(user)
