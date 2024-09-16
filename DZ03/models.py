from peewee import Model, CharField, IntegerField, FloatField, ForeignKeyField, SqliteDatabase
db = SqliteDatabase('students.db')
class Student(Model):
    name = CharField(null=False)  
    age = IntegerField(null=True)  
    gender = CharField(null=True) 
    group = CharField(null=True)  
    telegram_id = IntegerField(unique=True)  
    average_grade = FloatField(default=0.0)  

    class Meta:
        database = db
class Grade(Model):
    student = ForeignKeyField(Student, backref='grades')  
    subject = CharField()  
    grade = FloatField()   
    class Meta:
        database = db
db.connect()
db.create_tables([Student, Grade])