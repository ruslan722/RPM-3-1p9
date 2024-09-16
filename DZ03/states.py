from aiogram.fsm.state import State, StatesGroup
class StudentForm(StatesGroup):
    name = State()
    age = State()
    select_student = State()  
    enter_subject = State()  
    enter_grade = State()     