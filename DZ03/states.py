from aiogram.fsm.state import State, StatesGroup

class StudentForm(StatesGroup):
    choose_add_option = State()  
    telegram_id = State()     
    choose_data_option = State()
    name = State()              
    age = State()               
    gender = State()             
    group = State()              
    select_student = State()     
    enter_subject = State()      
    enter_grade = State()      