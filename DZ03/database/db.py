from peewee import SqliteDatabase
from models import Student

db = SqliteDatabase('students.db')

def create_tables():
    db.connect()
    db.create_tables([Student])

create_tables()
