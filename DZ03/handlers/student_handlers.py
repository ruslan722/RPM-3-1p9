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

# Обработка добавления студента по ID с последующим выбором: вводить ли данные или нет
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

        # Сохраняем ID студента в состоянии
        await state.update_data(telegram_id=telegram_id)

        # Предлагаем ввести дополнительные данные или оставить только ID
        options_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Да, ввести данные")],
                [KeyboardButton(text="Нет, сохранить только ID")],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Вы хотите ввести дополнительные данные о студенте?", reply_markup=options_keyboard)
        await state.set_state(StudentForm.choose_data_option)

    except ValueError:
        await message.answer("Введите корректный Telegram ID или пересылайте сообщение от студента.")

# Обработка выбора: ввести данные или сохранить только ID
@router.message(StudentForm.choose_data_option)
async def choose_data_option(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    if message.text == "Да, ввести данные":
        await add_student_start(message, state)  # Переходим к запросу данных
    elif message.text == "Нет, сохранить только ID":
        data = await state.get_data()
        telegram_id = data['telegram_id']

        # Добавляем студента с только ID, именем по умолчанию и возрастом по умолчанию (например, 0)
        Student.create(telegram_id=telegram_id, name="Не указано", age=0)

        # Отправляем кликабельную ссылку на профиль
        telegram_profile_link = f"<a href='tg://user?id={telegram_id}'>Профиль студента</a>"
        await message.answer(
            f"Студент с ID {telegram_id} добавлен. Имя не указано. Возраст: 0.\n"
            f"{telegram_profile_link}",
            parse_mode="HTML"
        )
        await state.clear()
    else:
        await message.answer("Пожалуйста, выберите корректный вариант.")

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
    await message.answer("Введите группу студента (например: 3-1П9):")
    await state.set_state(StudentForm.group)

# Запрос группы
@router.message(StudentForm.group)
async def set_student_group(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    group = message.text

    # Проверка формата группы (например, 3-1П9)
    if not group[0].isdigit() or not '-' in group or len(group.split('-')[1]) < 2:
        await message.answer("Пожалуйста, введите корректный формат группы (например: 3-1П9).")
        return

    # Сохранение данных в базу данных
    data = await state.get_data()
    name = data['name']
    age = data['age']
    gender = data['gender']
    telegram_id = data['telegram_id']  # Берем Telegram ID из состояния

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
            telegram_profile_link = f"<a href='tg://user?id={student.telegram_id}'>Профиль студента</a>"
            info += (f"Имя: {student.name}, Возраст: {student.age}, Пол: {student.gender}, "
                     f"Группа: {student.group}, Средняя оценка: {student.average_grade}, "
                     f"Telegram ID: {student.telegram_id}\n"
                     f"{telegram_profile_link}\n")
        await message.answer(info, parse_mode="HTML")
    else:
        await message.answer("Студентов нет.")

# Показать лучшего студента
@router.message(lambda message: message.text == "Показать лучшего студента")
async def show_best_student(message: Message):
    best_student = Student.select().order_by(Student.average_grade.desc()).first()
    if best_student:
        telegram_profile_link = f"<a href='tg://user?id={best_student.telegram_id}'>Профиль студента</a>"
        await message.answer(
            f"Лучший студент: {best_student.name}, Средняя оценка: {best_student.average_grade}\n"
            f"{telegram_profile_link}",
            parse_mode="HTML"
        )
    else:
        await message.answer("Студентов нет.")

# Сортировать студентов по средней оценке
@router.message(lambda message: message.text == "Сортировать студентов по средней оценке")
async def sort_students_by_average_grade(message: Message):
    students = Student.select().order_by(Student.average_grade.desc())  # Сортировка по убыванию средней оценки
    if students:
        info = ""
        for student in students:
            telegram_profile_link = f"<a href='tg://user?id={student.telegram_id}'>Профиль студента</a>"
            info += (f"Имя: {student.name}, Возраст: {student.age}, Пол: {student.gender}, "
                     f"Группа: {student.group}, Средняя оценка: {student.average_grade}\n"
                     f"{telegram_profile_link}\n")
        await message.answer(f"Студенты, отсортированные по средней оценке:\n{info}", parse_mode="HTML")
    else:
        await message.answer("Студентов нет.")

# Добавить оценку студенту (используем реальный Telegram ID)
@router.message(lambda message: message.text == "Добавить оценку студенту")
async def choose_student_for_grade(message: Message, state: FSMContext):
    students = Student.select()
    if not students:
        await message.answer("Нет студентов для добавления оценки.")
        return

    # Показываем список студентов с их реальными Telegram ID
    student_list = "\n".join([f"{student.name} (Telegram ID: {student.telegram_id})" for student in students])
    await message.answer(f"Выберите студента, отправив его Telegram ID:\n{student_list}")
    await state.set_state(StudentForm.select_student)

# Обработка выбора студента по его Telegram ID
@router.message(StudentForm.select_student)
async def enter_subject_for_grade(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    try:
        # Проверка, существует ли студент с таким Telegram ID
        telegram_id = int(message.text)
        student = Student.get_or_none(Student.telegram_id == telegram_id)
        if student:
            await state.update_data(telegram_id=telegram_id)  # Сохраняем Telegram ID студента
            await message.answer(f"Введите предмет для студента {student.name}:")
            await state.set_state(StudentForm.enter_subject)
        else:
            await message.answer("Неверный Telegram ID студента. Попробуйте еще раз.")
    except ValueError:
        await message.answer("Введите корректный Telegram ID студента.")

# Запрос предмета и сохранение оценки
@router.message(StudentForm.enter_subject)
async def enter_grade_for_subject(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    subject = message.text
    await state.update_data(subject=subject)
    await message.answer("Введите оценку (например: 4.5):")
    await state.set_state(StudentForm.enter_grade)

# Сохранение оценки
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
    telegram_id = data['telegram_id']  # Получаем Telegram ID студента
    subject = data['subject']

    # Сохраняем оценку в таблице Grade, используя Telegram ID
    Grade.create(student_id=telegram_id, subject=subject, grade=grade_value)

    # Пересчитываем среднюю оценку студента
    student = Student.get(Student.telegram_id == telegram_id)
    grades = Grade.select().where(Grade.student_id == telegram_id)
    average_grade = sum([g.grade for g in grades]) / len(grades)
    student.average_grade = average_grade
    student.save()

    await message.answer(f"Оценка {grade_value} по предмету {subject} добавлена для студента {student.name}. Средняя оценка обновлена.")
    await state.clear()
# Регистрация обработчиков
def register_handlers(dp):
    dp.include_router(router)