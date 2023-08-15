from models.user import User, UserModel
from config.jwt_manager import create_token
from models.user import Credentials
from datetime import datetime
from config.utils import now_date
import bcrypt

class UserService():

    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, email):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        return result

    def create_user(self, user: Credentials) -> bool:
        add_user: UserModel = UserModel(**user.dict())
        credentials: Credentials = Credentials(**user.dict())
        add_user.role: int = 0
        add_user.token: str = create_token(credentials.dict())
        add_user.created_at: datetime = now_date()
        add_user.token_expires: str = 'infinity'
        try: 
            self.db.add(add_user)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_user(self, id: int):
       self.db.query(UserModel).filter(UserModel.id == id).delete()
       self.db.commit()
       return
    
    def hash_password(self, password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    