from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from models import Student, Grade
from states import StudentForm
from keyboards.main_menu import main_menu_keyboard

router = Router()

# Команда /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Выберите действие:", reply_markup=main_menu_keyboard())

# Кнопка "Назад" - возврат в главное меню
@router.message(lambda message: message.text == "Назад")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()  # Очищаем текущее состояние
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_keyboard())

# Добавить студента - выбор варианта
@router.message(lambda message: message.text == "Добавить студента")
async def choose_add_student_option(message: Message, state: FSMContext):
    # Клавиатура с двумя вариантами и кнопкой "Назад"
    options_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить по ID")],
            [KeyboardButton(text="Добавить с запросом данных")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите способ добавления студента:", reply_markup=options_keyboard)
    await state.set_state(StudentForm.choose_add_option)

# Обработка выбора варианта
@router.message(StudentForm.choose_add_option)
async def handle_add_student_option(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    if message.text == "Добавить по ID":
        await message.answer("Перешлите сообщение от студента или введите его ID:")
        await state.set_state(StudentForm.telegram_id)
    elif message.text == "Добавить с запросом данных":
        await add_student_start(message, state)
    else:
        await message.answer("Пожалуйста, выберите корректный вариант.")

# Обработка добавления студента по ID с именем по умолчанию и ссылкой на профиль
@router.message(StudentForm.telegram_id)
async def process_telegram_id(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    try:
        if message.forward_from:  # Если пользователь переслал сообщение
            telegram_id = message.forward_from.id
        else:
            telegram_id = int(message.text)

        # Проверка, существует ли студент с таким Telegram ID
        existing_student = Student.get_or_none(Student.telegram_id == telegram_id)
        if existing_student:
            await message.answer(f"Студент с ID Telegram {telegram_id} уже существует.")
            await state.clear()
            return

        # Создаем ссылку на профиль студента
        telegram_profile_link = f"tg://user?id={telegram_id}"

        # Добавляем студента с только ID, именем по умолчанию и возрастом по умолчанию (например, 0)
        Student.create(telegram_id=telegram_id, name="Не указано", age=0)

        await message.answer(
            f"Студент с ID {telegram_id} добавлен. Имя не указано. Возраст: 0.\n"
            f"Профиль: [Ссылка на профиль студента]({telegram_profile_link})",
            parse_mode="Markdown"  # Используем Markdown для форматирования ссылки
        )
        await state.clear()

    except ValueError:
        await message.answer("Введите корректный Telegram ID или пересылайте сообщение от студента.")

# Начало добавления студента с запросом данных
async def add_student_start(message: Message, state: FSMContext):
    # Клавиатура с кнопкой "Назад"
    back_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Введите имя студента:", reply_markup=back_keyboard)
    await state.set_state(StudentForm.name)

# Запрос имени
@router.message(StudentForm.name)
async def set_student_name(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    await state.update_data(name=message.text)
    await message.answer("Введите возраст студента:")
    await state.set_state(StudentForm.age)

# Запрос возраста
@router.message(StudentForm.age)
async def set_student_age(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    try:
        age = int(message.text)
        await state.update_data(age=age)

        # Клавиатура для выбора пола с кнопкой "Назад"
        gender_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Выберите пол студента:", reply_markup=gender_keyboard)
        await state.set_state(StudentForm.gender)

    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")

# Запрос пола
@router.message(StudentForm.gender)
async def set_student_gender(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    gender = message.text
    if gender not in ["Мужской", "Женский"]:
        await message.answer("Пожалуйста, выберите пол из предложенных вариантов.")
        return

    await state.update_data(gender=gender)
    await message.answer("Введите группу студента:")
    await state.set_state(StudentForm.group)

# Запрос группы
@router.message(StudentForm.group)
async def set_student_group(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    group = message.text

    # Проверка формата группы 
    if not group[0].isdigit() or not '-' in group or len(group.split('-')[1]) < 2:
        await message.answer("Пожалуйста, введите корректный формат группы (например: 3-1П9).")
        return

    # Сохранение данных в базу данных
    data = await state.get_data()
    name = data['name']
    age = data['age']
    gender = data['gender']
    telegram_id = message.from_user.id  # Сохраняем Telegram ID пользователя

    # Проверяем, существует ли студент с таким Telegram ID
    existing_student = Student.get_or_none(Student.telegram_id == telegram_id)
    if existing_student:
        await message.answer(f"Студент с ID Telegram {telegram_id} уже существует.")
        await state.clear()
        return

    # Добавление студента в базу
    Student.create(name=name, age=age, gender=gender, group=group, telegram_id=telegram_id)

    await message.answer(f"Студент {name} добавлен.")
    await state.clear()

# Показать информацию о студентах
@router.message(lambda message: message.text == "Показать информацию о студентах")
async def show_students(message: Message):
    students = Student.select()
    if students:
        info = ""
        for student in students:
            info += f"Имя: {student.name}, Возраст: {student.age}, Пол: {student.gender}, Группа: {student.group}, Средняя оценка: {student.average_grade}, Telegram ID: {student.telegram_id}\n"
        await message.answer(info)
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

# Сортировать студентов по средней оценке
@router.message(lambda message: message.text == "Сортировать студентов по средней оценке")
async def sort_students_by_average_grade(message: Message):
    students = Student.select().order_by(Student.average_grade.desc())  # Сортировка по убыванию средней оценки
    if students:
        info = ""
        for student in students:
            info += f"Имя: {student.name}, Возраст: {student.age}, Пол: {student.gender}, Группа: {student.group}, Средняя оценка: {student.average_grade}\n"
        await message.answer(f"Студенты, отсортированные по средней оценке:\n{info}")
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
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

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
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    subject = message.text
    await state.update_data(subject=subject)
    await message.answer("Введите оценку:")
    await state.set_state(StudentForm.enter_grade)

@router.message(StudentForm.enter_grade)
async def save_grade(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return
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