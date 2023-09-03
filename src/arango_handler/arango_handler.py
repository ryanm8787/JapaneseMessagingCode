from pyArango.connection import *
import random

class Arangohandler:
    def __init__(self, name, username, password):
        self.db_name = name
        self.user_name = username
        self.password = password

    def __get_connection(self) -> Connection:
        self.conn = Connection(username=self.user_name, password=self.password)
        self.db = self.conn[self.db_name]

    def insert_row(self, word) -> None:
        db = self.__get_connection()
        word_conn = db.collections["tango"]
        doc = word_conn.createDocument(word)
        doc.save()

    def get_word(self) -> dict:
        db = self.__get_connection()
        indx = random.randint(0, len(db.count()))
        db[]
        return {}


def create_database(uname, password, db_name, db_collection) -> None:
    conn = Connection(username=uname, password=password)
    db = conn.createDatabase(name=db_name)
    db.createCollection(name=db_collection)

