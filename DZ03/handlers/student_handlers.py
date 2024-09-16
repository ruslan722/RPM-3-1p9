from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from models import Student, Grade
from states import StudentForm
from keyboards.main_menu import main_menu_keyboard

router = Router()

# Команда /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Выберите действие:", reply_markup=main_menu_keyboard())

# Добавить студента
@router.message(lambda message: message.text == "Добавить студента")
async def add_student_start(message: Message, state: FSMContext):
    await message.answer("Введите имя студента:")
    await state.set_state(StudentForm.name)

@router.message(StudentForm.name)
async def set_student_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите возраст студента:")
    await state.set_state(StudentForm.age)

@router.message(StudentForm.age)
async def set_student_age(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    try:
        age = int(message.text)
        student = Student.create(name=name, age=age)
        await message.answer(f"Студент {name} добавлен.")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")

# Показать информацию о студентах
@router.message(lambda message: message.text == "Показать информацию о студентах")
async def show_students(message: Message):
    students = Student.select()
    if students:
        info = ""
        for student in students:
            info += f"Имя: {student.name}, Возраст: {student.age}, Средняя оценка: {student.average_grade}\n"
        await message.answer(info)
    else:
        await message.answer("Студентов нет.")

# Сортировать студентов по средней оценке
@router.message(lambda message: message.text == "Сортировать студентов по средней оценке")
async def sort_students_by_average_grade(message: Message):
    students = Student.select().order_by(Student.average_grade.desc())  # Сортировка по убыванию средней оценки
    if students:
        info = ""
        for student in students:
            info += f"Имя: {student.name}, Возраст: {student.age}, Средняя оценка: {student.average_grade}\n"
        await message.answer(f"Студенты, отсортированные по средней оценке:\n{info}")
    else:
        await message.answer("Студентов нет.")

# Показать лучшего студента
@router.message(lambda message: message.text == "Показать лучшего студента")
async def show_best_student(message: Message):
    best_student = Student.select().order_by(Student.average_grade.desc()).first()
    if best_student:
        await message.answer(f"Лучший студент: {best_student.name}, Средняя оценка: {best_student.average_grade}")
    else:
        await message.answer("Студентов нет.")

# Добавить оценку студенту
@router.message(lambda message: message.text == "Добавить оценку студенту")
async def choose_student_for_grade(message: Message, state: FSMContext):
    students = Student.select()
    if not students:
        await message.answer("Нет студентов для добавления оценки.")
        return

    # Показываем список студентов для выбора
    student_list = "\n".join([f"{student.id}. {student.name}" for student in students])
    await message.answer(f"Выберите студента, отправив его ID:\n{student_list}")
    await state.set_state(StudentForm.select_student)

@router.message(StudentForm.select_student)
async def enter_subject_for_grade(message: Message, state: FSMContext):
    try:
        student_id = int(message.text)
        student = Student.get_or_none(Student.id == student_id)
        if student:
            await state.update_data(student_id=student_id)
            await message.answer(f"Введите предмет для студента {student.name}:")
            await state.set_state(StudentForm.enter_subject)
        else:
            await message.answer("Неверный ID студента. Попробуйте еще раз.")
    except ValueError:
        await message.answer("Введите корректный ID студента.")

@router.message(StudentForm.enter_subject)
async def enter_grade_for_subject(message: Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)
    await message.answer("Введите оценку: ")
    await state.set_state(StudentForm.enter_grade)

@router.message(StudentForm.enter_grade)
async def save_grade(message: Message, state: FSMContext):
    try:
        grade_value = float(message.text)
    except ValueError:
        await message.answer("Введите корректное число.")
        return

    # Получаем данные из состояния
    data = await state.get_data()
    student_id = data['student_id']
    subject = data['subject']

    # Сохраняем оценку
    student = Student.get(Student.id == student_id)
    Grade.create(student=student, subject=subject, grade=grade_value)

    # Пересчитываем среднюю оценку
    grades = Grade.select().where(Grade.student == student)
    average_grade = sum([g.grade for g in grades]) / len(grades)
    student.average_grade = average_grade
    student.save()

    await message.answer(f"Оценка {grade_value} по предмету {subject} добавлена для студента {student.name}. Средняя оценка обновлена.")
    await state.clear()
# Регистрация обработчиков
def register_handlers(dp):
    dp.include_router(router)