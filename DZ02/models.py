from peewee import *

# Подключение к базе данных SQLite
db = SqliteDatabase('library.db')

# Модель книги
class Book(Model):
    title = CharField()
    author = CharField()
    year = IntegerField()
    pages = IntegerField()
    dostup = BooleanField(default=True)

    class Meta:
        database = db  # Подключение к базе данных

# Функция для инициализации базы данных и создания таблиц
def biblioteka():
    db.connect()
    db.create_tables([Book], safe=True)


