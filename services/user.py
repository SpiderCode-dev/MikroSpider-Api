from models.user import User, UserModel


class UserService():

    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, id):
        result = self.db.query(UserModel).filter(UserModel.id == id).first()
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