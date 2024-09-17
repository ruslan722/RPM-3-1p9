from peewee import SqliteDatabase
from models import Student, Grade

db = SqliteDatabase('students.db')

def create_tables():
    db.connect()
    db.create_tables([Student, Grade])  # Создаём таблицы

create_tables()