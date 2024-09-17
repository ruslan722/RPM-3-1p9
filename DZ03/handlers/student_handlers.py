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
    
    data = await state.get_data()
    telegram_id = data.get('telegram_id', None)  # Здесь мы получаем Telegram ID, но это поле может быть пустым

    if message.text == "Да, ввести данные":
        await add_student_start(message, state)  # Переходим к запросу данных
    elif message.text == "Нет, сохранить только ID":
        if telegram_id is None:
            # Добавляем студента без Telegram ID, но с обязательными полями
            Student.create(name="Не указано", age=0, gender="Не указано", group="Не указано")
            await message.answer("Студент добавлен без Telegram ID.")
        else:
            Student.create(telegram_id=telegram_id, name="Не указано", age=0)
            await message.answer(f"Студент с ID {telegram_id} добавлен.")

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
    if not group[0].isdigit() or '-' not in group or len(group.split('-')[1]) < 2:
        await message.answer("Пожалуйста, введите корректный формат группы.")
        return

    data = await state.get_data()
    name = data['name']
    age = data['age']
    gender = data['gender']
    telegram_id = data.get('telegram_id', None)

    existing_student = Student.get_or_none(Student.telegram_id == telegram_id)
    if existing_student:
        await message.answer(f"Студент с ID Telegram {telegram_id} уже существует.")
        await state.clear()
        return
    if telegram_id is None:
        Student.create(name=name, age=age, gender=gender, group=group)
        await message.answer(f"Студент {name} добавлен без Telegram ID.")
    else:
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
# Просмотр оценок студента (Telegram ID или имя)
@router.message(lambda message: message.text == "Посмотреть оценки студента")
async def choose_student_for_view_grades(message: Message, state: FSMContext):
    students = Student.select()
    if not students:
        await message.answer("Нет студентов для просмотра оценок.")
        return

    # Отображаем список студентов с именем и ID, если он есть
    student_list = "\n".join([f"{student.name} (Telegram ID: {student.telegram_id if student.telegram_id else 'None'})"
                              for student in students])
    await message.answer(f"Выберите студента, отправив его Telegram ID или имя (если ID отсутствует):\n{student_list}")
    await state.set_state(StudentForm.select_student_for_view)

# Вывод таблицы оценок студента (по Telegram ID или имени)
@router.message(StudentForm.select_student_for_view)
async def show_student_grades(message: Message, state: FSMContext):
    input_text = message.text
    student = None

    try:
        # Попробуем интерпретировать ввод как Telegram ID
        telegram_id = int(input_text)
        student = Student.get_or_none(Student.telegram_id == telegram_id)
    except ValueError:
        # Если не удалось преобразовать в ID, ищем студента по имени
        student = Student.get_or_none(Student.name == input_text)

    if not student:
        await message.answer("Неверный Telegram ID или имя студента. Попробуйте еще раз.")
        return

    # Получаем оценки студента
    grades = Grade.select().where(Grade.student_id == student.id)
    if grades:
        grade_info = "Оценки студента:\n"
        grade_info += "{:<10} {:<10}\n".format("Предмет", "Оценка")
        grade_info += "-" * 20 + "\n"
        for grade in grades:
            grade_info += f"{grade.subject:<10} {grade.grade:<10}\n"

        await message.answer(grade_info)
        await state.update_data(student_id=student.id)  # Сохраняем ID студента для будущих операций

        # Спрашиваем, что делать дальше (изменить оценку или добавить новую)
        options_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Изменить оценку")],
                [KeyboardButton(text="Добавить новую оценку")],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Что вы хотите сделать?", reply_markup=options_keyboard)
        await state.set_state(StudentForm.grade_action)
    else:
        await message.answer("У студента нет оценок.")
# Просмотр оценок студента
@router.message(lambda message: message.text == "Посмотреть оценки студента")
async def choose_student_for_view_grades(message: Message, state: FSMContext):
    students = Student.select()
    if not students:
        await message.answer("Нет студентов для просмотра оценок.")
        return

    student_list = "\n".join([f"{student.name} (Telegram ID: {student.telegram_id})" for student in students])
    await message.answer(f"Выберите студента, отправив его Telegram ID:\n{student_list}")
    await state.set_state(StudentForm.select_student_for_view)

# Вывод таблицы оценок студента
@router.message(StudentForm.select_student_for_view)
async def show_student_grades(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        student = Student.get_or_none(Student.telegram_id == telegram_id)

        if not student:
            await message.answer("Неверный Telegram ID студента. Попробуйте еще раз.")
            return

        grades = Grade.select().where(Grade.student_id == telegram_id)
        if grades:
            grade_info = "Оценки студента:\n"
            grade_info += "{:<10} {:<10}\n".format("Предмет", "Оценка")
            grade_info += "-" * 20 + "\n"
            for grade in grades:
                grade_info += f"{grade.subject:<10} {grade.grade:<10}\n"

            await message.answer(grade_info)
            await state.update_data(telegram_id=telegram_id)

            options_keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Изменить оценку")],
                    [KeyboardButton(text="Добавить новую оценку")],
                    [KeyboardButton(text="Назад")]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await message.answer("Что вы хотите сделать?", reply_markup=options_keyboard)
            await state.set_state(StudentForm.grade_action)
        else:
            await message.answer("У студента нет оценок.")
    except ValueError:
        await message.answer("Введите корректный Telegram ID студента.")

# Действие с оценками (изменить или добавить)
@router.message(StudentForm.grade_action)
async def handle_grade_action(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    if message.text == "Изменить оценку":
        await message.answer("Введите название предмета для изменения оценки:")
        await state.set_state(StudentForm.change_grade_subject)
    elif message.text == "Добавить новую оценку":
        await message.answer("Введите название предмета для добавления новой оценки:")
        await state.set_state(StudentForm.add_new_subject)
    else:
        await message.answer("Пожалуйста, выберите корректный вариант.")

# Изменение оценки: запрос предмета
@router.message(StudentForm.change_grade_subject)
async def request_new_grade(message: Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)
    await message.answer("Введите новую оценку:")
    await state.set_state(StudentForm.change_grade_value)

# Изменение оценки: запрос новой оценки и сохранение
@router.message(StudentForm.change_grade_value)
async def save_new_grade(message: Message, state: FSMContext):
    try:
        new_grade = float(message.text)
        data = await state.get_data()
        
        # Проверка наличия telegram_id
        telegram_id = data.get('telegram_id', None)
        student_id = data.get('student_id')

        if not student_id:
            await message.answer("Ошибка: Не найден ID студента.")
            return

        subject = data['subject']

        # Получаем студента
        student = Student.get_or_none(Student.id == student_id)

        # Ищем оценку для изменения
        grade = Grade.get_or_none(Grade.student_id == student_id, Grade.subject == subject)
        if grade:
            grade.grade = new_grade
            grade.save()

            # Пересчитываем среднюю оценку
            grades = Grade.select().where(Grade.student_id == student.id)
            average_grade = sum([g.grade for g in grades]) / len(grades)
            student.average_grade = average_grade
            student.save()

            await message.answer(f"Оценка по предмету {subject} изменена на {new_grade}. Средняя оценка обновлена.")
            await state.clear()
        else:
            await message.answer(f"Оценка по предмету {subject} не найдена.")
    except ValueError:
        await message.answer("Введите корректное число.")

# Добавление новой оценки: запрос предмета
@router.message(StudentForm.add_new_subject)
async def request_new_subject_grade(message: Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)
    await message.answer("Введите оценку:")
    await state.set_state(StudentForm.add_new_grade)

# Добавление новой оценки: сохранение
@router.message(StudentForm.add_new_grade)
async def save_new_subject_grade(message: Message, state: FSMContext):
    try:
        new_grade = float(message.text)
        data = await state.get_data()

        # Проверка наличия telegram_id и student_id
        telegram_id = data.get('telegram_id', None)
        student_id = data.get('student_id')

        if not student_id:
            await message.answer("Ошибка: Не найден ID студента.")
            return

        subject = data['subject']

        # Добавляем новую оценку
        Grade.create(student_id=student_id, subject=subject, grade=new_grade)

        # Пересчитываем среднюю оценку
        student = Student.get(Student.id == student_id)
        grades = Grade.select().where(Grade.student_id == student_id)
        average_grade = sum([g.grade for g in grades]) / len(grades)
        student.average_grade = average_grade
        student.save()

        await message.answer(f"Оценка по предмету {subject} добавлена: {new_grade}. Средняя оценка обновлена.")
        await state.clear()
    except ValueError:
        await message.answer("Введите корректное число.")
# Функция для повторного выбора действия с оценками
async def ask_for_next_grade_action(message: Message, state: FSMContext):
    options_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить оценку")],
            [KeyboardButton(text="Добавить новую оценку")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Что вы хотите сделать дальше?", reply_markup=options_keyboard)
    await state.set_state(StudentForm.grade_action)
# Добавить оценку студенту (используем реальный Telegram ID)
@router.message(lambda message: message.text == "Добавить оценку студенту")
async def choose_student_for_grade(message: Message, state: FSMContext):
    students = Student.select()
    if not students:
        await message.answer("Нет студентов для добавления оценки.")
        return

    student_list = "\n".join([f"{student.name} (Telegram ID: {student.telegram_id})" for student in students])
    await message.answer(f"Выберите студента, отправив его Telegram ID:\n{student_list}")
    await state.set_state(StudentForm.select_student)

# Добавить оценку студенту (используем реальный Telegram ID или имя, если Telegram ID отсутствует)
@router.message(lambda message: message.text == "Добавить оценку студенту")
async def choose_student_for_grade(message: Message, state: FSMContext):
    students = Student.select()
    if not students:
        await message.answer("Нет студентов для добавления оценки.")
        return

    student_list = "\n".join([f"{student.name} (Telegram ID: {student.telegram_id})" if student.telegram_id 
                              else f"{student.name} (Telegram ID отсутствует)" for student in students])
    await message.answer(f"Выберите студента, отправив его Telegram ID или имя (если ID отсутствует):\n{student_list}")
    await state.set_state(StudentForm.select_student)

# Обработка выбора студента по его Telegram ID или имени
@router.message(StudentForm.select_student)
async def enter_subject_for_grade(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    input_text = message.text
    student = None

    try:
        # Попробуем интерпретировать ввод как Telegram ID
        telegram_id = int(input_text)
        student = Student.get_or_none(Student.telegram_id == telegram_id)
    except ValueError:
        # Если не удалось преобразовать в ID, ищем студента по имени
        student = Student.get_or_none(Student.name == input_text)

    if student:
        await state.update_data(student_id=student.id, student_name=student.name)  # Сохраняем ID студента
        await message.answer(f"Введите предмет для студента {student.name}:")
        await state.set_state(StudentForm.enter_subject)
    else:
        await message.answer("Неверный Telegram ID или имя студента. Попробуйте еще раз.")

# Запрос предмета и сохранение оценки
@router.message(StudentForm.enter_subject)
async def enter_grade_for_subject(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    subject = message.text
    await state.update_data(subject=subject)
    await message.answer("Введите оценку:")
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

    data = await state.get_data()
    student_id = data['student_id']
    subject = data['subject']

    # Сохраняем оценку
    Grade.create(student_id=student_id, subject=subject, grade=grade_value)

    # Пересчитываем среднюю оценку
    student = Student.get(Student.id == student_id)
    grades = Grade.select().where(Grade.student_id == student_id)
    average_grade = sum([g.grade for g in grades]) / len(grades)
    student.average_grade = average_grade
    student.save()

    await message.answer(f"Оценка {grade_value} по предмету {subject} добавлена для студента {student.name}. Средняя оценка обновлена.")
    await state.clear()


# Обработка выбора студента по его Telegram ID
@router.message(StudentForm.select_student)
async def enter_subject_for_grade(message: Message, state: FSMContext):
    if message.text == "Назад":
        await back_to_menu(message, state)
        return

    try:
        telegram_id = int(message.text)
        student = Student.get_or_none(Student.telegram_id == telegram_id)
        if student:
            await state.update_data(telegram_id=telegram_id)
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
    await message.answer("Введите оценку:")
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

    data = await state.get_data()
    telegram_id = data['telegram_id']
    subject = data['subject']

    Grade.create(student_id=telegram_id, subject=subject, grade=grade_value)

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