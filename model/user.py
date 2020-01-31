from database import SQLite
from errors import ApplicationError

from itsdangerous import(
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)

SECRET_KEY = 'r7R9RhGgDPvvWl3iNzLuIIfELmo'

class User(object):

    def __init__(self, username, password, email, address, phone_number, user_id=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.address = address
        self.phone_number = phone_number

    def to_dict(self):
        user_data = self.__dict__
        del user_data["password"]
        return user_data

    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.user_id = cursor.lastrowid
        return self

    @staticmethod
    def delete(user_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM user WHERE user_id = ?",
                    (user_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find(user_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password,  email, address, phone_number, user_id FROM user WHERE user_id = ?",
                    (user_id,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "User with id {} not found".format(user_id), 404)
        return User(*user)

    @staticmethod
    def find_by_email(email):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password,  email, address, phone_number, user_id FROM user WHERE email = ?",
                    (email,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "User with name {} not found".format(username), 404)
        return User(*user)
    
    def generate_token(self):
        s = Serializer(SECRET_KEY)
        return s.dumps({'user_id': self.user_id})
    
    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except BadSignature:
            return False
        return s.loads(token)['user_id']
    
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password, email, address, phone_number, user_id FROM user").fetchall()
            return [User(*row) for row in result]

    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.user_id == None:
            args = (self.username, self.password, self.email, self.address, self.phone_number)
            query = query.format("INSERT", "(username, password, email, address, phone_number)", args)
        else:
            args = (self.user_id, self.username, self.password, self.email, self.address, self.phone_number)
            query = query.format("REPLACE", "(user_id, username, password, email, address, phone_number)", args)
        return query

