from aiogram.fsm.state import State, StatesGroup

class StudentForm(StatesGroup):
    choose_add_option = State()  # Выбор между добавлением по ID и запросом данных
    telegram_id = State()        # Для получения Telegram ID
    name = State()               # Ввод имени студента
    age = State()                # Ввод возраста студента
    gender = State()             # Ввод пола студента
    group = State()              # Ввод группы студента
    select_student = State()     # Для выбора студента при добавлении оценки
    enter_subject = State()      # Ввод предмета для оценки
    enter_grade = State()        # Ввод оценки
