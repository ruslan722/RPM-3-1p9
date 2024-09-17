from peewee import Model, CharField, IntegerField, FloatField, ForeignKeyField, BigIntegerField, SqliteDatabase

# Инициализация базы данных
db = SqliteDatabase('students.db')

# Модель для студентов
class Student(Model):
    name = CharField(null=True)  # Имя студента (может быть NULL)
    age = IntegerField(null=True)  # Возраст студента (может быть NULL)
    gender = CharField(null=True)  # Пол студента (может быть NULL)
    group = CharField(null=True)  # Группа студента
    telegram_id = BigIntegerField(unique=True)  # Telegram ID (уникальный и больше, чем обычный Integer)
    average_grade = FloatField(default=0.0)  # Средняя оценка студента

    class Meta:
        database = db  # Связываем модель с базой данных

# Модель для оценок
class Grade(Model):
    student = ForeignKeyField(Student, backref='grades', on_delete='CASCADE')  # Внешний ключ на студента
    subject = CharField()  # Название предмета
    grade = FloatField()  # Оценка

    class Meta:
        database = db  # Связываем модель с базой данных

# Функция для инициализации таблиц в базе данных
def init_db():
    with db:
        db.create_tables([Student, Grade])
    print("Таблицы успешно созданы.")

# Вызов функции для инициализации базы данных
init_db()