from database import SQLite
from errors import ApplicationError


class Ad(object):

    def __init__(self, creator_id, title, desc, price, date, buyer, is_available, ad_id=None):
        self.creator_id = creator_id
        self.ad_id = ad_id
        self.title = title
        self.desc = desc
        self.price = price
        self.date = date
        self.buyer = buyer
        self.is_available = is_available
        

    def to_dict(self):
        return self.__dict__

    def save(self):
        query = "{} INTO ad {} VALUES {}"
    
        if self.ad_id == None:
            query = query.format("INSERT", "(creator_id, title, desc, price, date, buyer, is_available)", "(?, ?, ?, ?, ?, ?, ?)")
            args = (self.creator_id, self.title, self.desc, self.price, self.date, self.buyer, self.is_available) 
        else:
            query = query.format("REPLACE", "(creator_id, ad_id, title, desc, price, date, buyer, is_available)", "(?, ?, ?, ?, ?, ?, ?, ?)")
            args = (self.creator_id, self.ad_id, self.title, self.desc, self.price, self.date, self.buyer, self.is_available)
        
        with SQLite() as db:
            cursor = db.execute(query, args)
            self.ad_id = cursor.lastrowid
        return self

    @staticmethod
    def delete(ad_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM ad WHERE ad_id = ?",
                    (ad_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find_by_id(ad_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                        "SELECT creator_id, title, desc, price, date, buyer, is_available, ad_id FROM ad WHERE ad_id = ?",
                        (ad_id,))
                        
        ad = result.fetchone()
        if ad is None:
            raise ApplicationError(
                    "Ad with id {} not found".format(ad_id), 404)
        return Ad(*ad)
    
    @staticmethod
    def find_all_purchased(creator_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT ad_id, title, desc, price, date, buyer FROM ad WHERE (creator_id = ? AND is_available = ?)",
                    (creator_id, 0))
        
        ad = result.fetchall()
        if ad is None:
            raise ApplicationError(
                    "User with id {} has no ads".format(creator_id), 404)
        return ad
    
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT creator_id, title, desc, price, date, buyer, is_available, ad_id FROM ad").fetchall()
            return [Ad(*row) for row in result]

