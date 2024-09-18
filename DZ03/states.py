from aiogram.fsm.state import State, StatesGroup

class StudentForm(StatesGroup):
    choose_add_option = State()  
    telegram_id = State()     
    choose_data_option = State()
    name = State()              
    age = State()               
    gender = State()             
    group = State()              
    select_student_for_view = State()  # Выбор студента для просмотра его оценок
    grade_action = State()  # Действие с оценками (изменить или добавить)
    change_grade_subject = State()  # Выбор предмета для изменения оценки
    change_grade_value = State()  # Ввод новой оценки
    add_new_subject = State()  # Ввод предмета для новой оценки
    add_new_grade = State()  # Ввод новой оценки
    select_student = State()     
    enter_subject = State()      
    enter_grade = State()      
  # Для цикла изменения/добавления оценок
    grade_action_cycle = State()  # Цикл действия с оценками (добавление/изменение)
    change_grade_subject_in_cycle = State()  # Изменение оценки в цикле: выбор предмета
    change_grade_value_in_cycle = State()  # Изменение оценки в цикле: ввод новой оценки
    add_new_subject_in_cycle = State()  # Добавление новой оценки в цикле: выбор предмета
    add_new_grade_in_cycle = State()  # Добавление новой оценки в цикле: ввод оценки