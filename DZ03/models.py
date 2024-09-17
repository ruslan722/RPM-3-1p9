from peewee import Model, CharField, IntegerField, FloatField, SqliteDatabase
# Инициализация базы данных
db = SqliteDatabase('students.db')
# Модель для студентов
class Student(Model):
    name = CharField(null=True)  # Имя студента (может быть NULL, если оно не указано)
    age = IntegerField(null=True)  # Возраст студента (может быть NULL)
    gender = CharField(null=True)  # Пол студента (может быть NULL)
    group = CharField(null=True)  # Группа студента 
    telegram_id = IntegerField(unique=True)  # Реальный Telegram ID студента (уникальный)
    average_grade = FloatField(default=0.0)  # Средняя оценка студента

    class Meta:
        database = db  # Связываем модель с базой данных

# Модель для оценок
class Grade(Model):
    student_id = IntegerField()  # Реальный Telegram ID студента
    subject = CharField()  # Название предмета
    grade = FloatField()  # Оценка

    class Meta:
        database = db  # Связываем модель с базой данных

# Функция для инициализации таблиц в базе данных
def init_db():
    with db:
        db.create_tables([Student, Grade])