import os  # Импортируем модуль os для определения операционной системы
from abc import ABC, abstractmethod  # Импортируем модуль для создания абстрактных классов
from typing import List  # Импортируем тип List для указания типов данных

# Абстрактный класс для базового функционала заказов
class OrderBase(ABC):
    total_order_count: int = 0  # Статический атрибут для хранения общего количества заказов

    def __init__(self, order_number: int, status: str = "В процессе"):
        self.order_number: int = order_number  # Номер заказа
        self.status: str = status  # Статус заказа
        OrderBase.total_order_count += 1  # Увеличиваем общий счетчик заказов при создании нового заказа

    @abstractmethod
    def display_info(self) -> None:
        """Абстрактный метод для отображения информации о заказе. Реализуется в подклассах."""
        pass

    @staticmethod
    def total_orders() -> int:
        """Статический метод для получения общего количества заказов"""
        return OrderBase.total_order_count

    def __str__(self) -> str:
        """Переопределенный метод для строкового представления объекта заказа"""
        return f"Заказ {self.order_number}, Статус: {self.status}"

# Класс для обычных заказов, наследует функционал от OrderBase
class Order(OrderBase):
    def __init__(self, order_number: int):
        super().__init__(order_number)  # Инициализация базового класса
        self.dishes: List[str] = []  # Список блюд в заказе

    def add_dish(self, dish: str) -> None:
        """Добавляет блюдо в заказ"""
        self.dishes.append(dish)
        print(f"Блюдо '{dish}' добавлено в заказ {self.order_number}")

    def change_status(self, status: str) -> None:
        """Изменяет статус заказа"""
        self.status = status
        print(f"Статус заказа {self.order_number} изменен на '{self.status}'")

    def display_info(self) -> None:
        """Отображает информацию о заказе"""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")

    def __str__(self) -> str:
        """Возвращает строковое представление заказа с блюдами"""
        return f"{super().__str__()}, Блюда: {', '.join(self.dishes)}"

# Класс для заказов с доставкой, наследует от OrderBase
class DeliveryOrder(OrderBase):
    def __init__(self, order_number: int, delivery_address: str, delivery_time: str):
        super().__init__(order_number)  # Инициализация базового класса
        self.delivery_address: str = delivery_address  # Адрес доставки
        self.delivery_time: str = delivery_time  # Время доставки
        self.dishes: List[str] = []  # Список блюд

    def display_info(self) -> None:
        """Отображает информацию о заказе с доставкой"""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")
        print(f"Адрес доставки: {self.delivery_address}")
        print(f"Время доставки: {self.delivery_time}")

    def __str__(self) -> str:
        """Возвращает строковое представление заказа с доставкой"""
        return (f"{super().__str__()}, Адрес доставки: {self.delivery_address}, "
                f"Время доставки: {self.delivery_time}")

# Функция для обработки Linux-команд
def linux_commands(orders: List[OrderBase], command: str) -> None:
    # Команда для создания нового заказа
    if command.startswith("touch"):
        parts = command.split()
        if len(parts) == 2:
            order_number = int(parts[1])
            new_order = Order(order_number)  # Создаем новый заказ
            orders.append(new_order)  # Добавляем его в список заказов
            print(f"Заказ {order_number} создан командой touch.")
        else:
            print("Ошибка: Использование команды 'touch <номер заказа>'.")

    # Команда для добавления блюда в заказ
    elif command.startswith("add"):
        parts = command.split()
        if len(parts) == 3:
            order_number = int(parts[1])
            dish = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order.add_dish(dish)  # Добавляем блюдо в заказ
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'add <номер заказа> <блюдо>'.")

    # Команда для изменения статуса заказа
    elif command.startswith("status"):
        parts = command.split()
        if len(parts) == 3:
            order_number = int(parts[1])
            new_status = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)  # Изменяем статус заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'status <номер заказа> <новый статус>'.")

    # Команда для вывода информации о заказе
    elif command.startswith("info"):
        parts = command.split()
        if len(parts) == 2:
            order_number = int(parts[1])
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()  # Отображаем информацию о заказе
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'info <номер заказа>'.")

    # Команда для вывода всех заказов
    elif command.startswith("list"):
        print("Список всех заказов:")
        for order in orders:
            print(order)

    # Команда для отображения общего количества заказов
    elif command.startswith("total"):
        print(f"Общее количество заказов: {OrderBase.total_orders()}")

# Функция для показа справки по Linux-командам
def show_linux_help() -> None:
    """Вывод доступных команд Linux"""
    print("\n--- Доступные команды Linux ---")
    print("1. 'touch <номер заказа>' - Создать новый заказ с указанным номером.")
    print("2. 'add <номер заказа> <блюдо>' - Добавить блюдо в заказ.")
    print("3. 'status <номер заказа> <новый статус>' - Изменить статус заказа.")
    print("4. 'info <номер заказа>' - Показать информацию о заказе.")
    print("5. 'list' - Показать все заказы.")
    print("6. 'total' - Показать общее количество заказов.")

# Функция главного меню программы
def main_menu() -> None:
    orders: List[OrderBase] = []  # Список заказов
    os_type = os.name  # Определяем тип операционной системы

    while True:
        print("\n--- Управление заказами ---")
        print("1. Создать заказ")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Показать общее количество заказов")
        if os_type == "posix":  # Если операционная система Linux/Unix
            print("7. Выполнить команду Linux")
            print("8. Показать справку по командам Linux")
        print("9. Выйти")
        choice = input("Выберите опцию: ")

        # Логика выполнения выбранных пользователем опций
        if choice == '1':
            order_type = input("Введите 'D' для заказа с доставкой или 'O' для обычного заказа: ").upper()
            order_number = int(input("Введите номер заказа: "))

            if order_type == 'D':  # Если заказ с доставкой
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(order_number, address, delivery_time)  # Создаем заказ с доставкой
            else:
                order = Order(order_number)  # Создаем обычный заказ

            orders.append(order)  # Добавляем заказ в список
            print(f"Заказ {order_number} создан.")

        elif choice == '2':
            order_number = int(input("Введите номер заказа: "))
            dish = input("Введите название блюда: ")
            for order in orders:
                if order.order_number == order_number:
                    order.add_dish(dish)  # Добавляем блюдо в заказ
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '3':
            order_number = int(input("Введите номер заказа: "))
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()  # Отображаем информацию о заказе
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '4':
            order_number = int(input("Введите номер заказа: "))
            new_status = input("Введите новый статус: ")
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)  # Изменяем статус заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '5':
            for order in orders:
                print(order)  # Отображаем все заказы

        elif choice == '6':
            print(f"Общее количество заказов: {OrderBase.total_orders()}")  # Отображаем общее количество заказов

        elif choice == '7' and os_type == "posix":
            command = input("Введите команду Linux для выполнения (например, 'touch', 'add', 'status', 'info', 'list', 'total'): ")
            linux_commands(orders, command)  # Выполнение команд Linux

        elif choice == '8' and os_type == "posix":
            show_linux_help()  # Отображаем справку по командам Linux

        elif choice == '9':
            print("Выход из программы.")
            break  # Выход из программы

        else:
            print("Неверный выбор. Попробуйте снова.")  # Обработка неправильного выбора

# Запуск программы
if __name__ == "__main__":
    main_menu()  # Запускаем главное меню

