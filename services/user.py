from models.user import User, UserModel
import bcrypt

class UserService():

    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, email):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        return result

    def create_user(self, user: User):
        add_user = UserModel(**user.dict())
        self.db.add(add_user)
        self.db.commit()
        return

    def delete_user(self, id: int):
       self.db.query(UserModel).filter(UserModel.id == id).delete()
       self.db.commit()
       return
    
    def hash_password(self, password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    