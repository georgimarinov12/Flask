from database import SQLite
from errors import ApplicationError


class Ad(object):

    def __init__(self, creator_id, title, desc, price, date, is_available=1, buyer, ad_id=None):
        self.creator_id
        self.id = ad_id
        self.title = title
        self.desc = desc
        self.price = price
        self.date = date
        self.is_available = is_available
        self.buyer = buyer

    def to_dict(self):
        return self.__dict__

    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self

    @staticmethod
    def delete(ad_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM post WHERE id = ?",
                    (ad_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find(ad_id):
        result = None
        with SQLite() as db:
            if self.is_available == 0:
                result = db.execute(
                        "SELECT title, desc, price, date, is_available, buyer, id FROM post WHERE id = ?",
                        (ad_id,))
            else:
                result = db.execute(
                        "SELECT title, desc, price, date, is_available, id FROM post WHERE id = ?",
                        (ad_id,))
        ad = result.fetchone()
        if ad is None:
            raise ApplicationError(
                    "Ad with id {} not found".format(ad_id), 404)
        return Ad(*ad)

    @staticmethod
    def all():
        with SQLite() as db:
            if self.is_available == 0:
                result = db.execute(
                        "SELECT title, desc, price, date, is_available, buyer, id FROM post").fetchall()
            else:
                result = db.execute(
                        "SELECT title, desc, price, date, is_available, id FROM post").fetchall()
            return [Ad(*row) for row in result]

    def __get_save_query(self):
        query = "{} INTO ad {} VALUES {}"
        if self.id == None:
            if self.is_available == 1:
                args = (self.creator_id, self.title, self.desc, self.price, self.date)
                query = query.format("INSERT", "(creator_id, title, desc, price, date)", args)
            else:
                args = (self.creator_id, self.title, self.desc, self.price, self.date, self.is_available, self.buyer)
                query = query.format("INSERT", "(creator_id, title, desc, price, date, is_available, buyer)", args)
        else:
            if self.is_available == 1:
                args = (self.id, self.title, self.desc, self.price, self.date)
                query = query.format("REPLACE", "(id, title, desc, price, date)", args)
            else:
                args = (self.title, self.desc, self.price, self.date, self.is_available, self.buyer)
                query = query.format("REPLACE", "(id, title, desc, price, date, is_available, buyer)", args)
        return query






