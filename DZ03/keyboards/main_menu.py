from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Добавить студента")
    builder.button(text="Добавить оценку студенту")
    builder.button(text="Показать информацию о студентах")
    builder.button(text="Сортировать студентов по средней оценке")
    builder.button(text="Показать лучшего студента")
    builder.adjust(2)  
    return builder.as_markup(resize_keyboard=True)
