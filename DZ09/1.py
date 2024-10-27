import os  # Импортируем модуль os для работы с операционной системой, чтобы определить тип системы.
from abc import ABC, abstractmethod  # Импортируем ABC и abstractmethod из модуля abc для создания абстрактных классов.

# Определение абстрактного базового класса для заказов
class OrderBase(ABC):
    total_order_count = 0  # Статический атрибут для хранения общего количества заказов.

    # Инициализация базового класса с номером заказа
    def __init__(self, order_number):
        self.order_number = order_number  # Устанавливаем номер заказа.
        self.status = "В процессе"  # Статус заказа по умолчанию "В процессе".
        OrderBase.total_order_count += 1  # Увеличиваем общее количество заказов на 1 при создании нового заказа.

    @abstractmethod
    def display_info(self):
        """Абстрактный метод для вывода информации о заказе."""
        pass  # Определяется в дочерних классах.

    @staticmethod
    def total_orders():
        """Выводит общее количество заказов."""
        print(f"Общее количество заказов: {OrderBase.total_order_count}")

    def __str__(self):
        """Строковое представление объекта заказа."""
        return f"Заказ {self.order_number}, Статус: {self.status}"


# Класс для обычных заказов, наследуется от OrderBase
class Order(OrderBase):
    def __init__(self, order_number):
        super().__init__(order_number)  # Инициализируем базовый класс.
        self.dishes = []  # Список блюд в заказе.

    def display_info(self):
        """Выводит подробную информацию о заказе."""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")  # Выводим список блюд, разделенный запятыми.
        print(f"Статус: {self.status}")  # Статус заказа.

    def add_dish(self, dish):
        """Добавляет блюдо в заказ."""
        self.dishes.append(dish)  # Добавляем блюдо в список блюд.
        print(f"Блюдо '{dish}' добавлено в заказ {self.order_number}")

    def change_status(self, status):
        """Изменяет статус заказа."""
        self.status = status  # Обновляем статус заказа.
        print(f"Статус заказа {self.order_number} изменен на '{self.status}'")

    def __str__(self):
        """Строковое представление заказа с включенными блюдами."""
        return f"{super().__str__()}, Блюда: {', '.join(self.dishes)}"

    def __add__(self, dish):
        """Перегрузка оператора + для добавления блюда."""
        self.add_dish(dish)  # Используем метод добавления блюда.
        return self  # Возвращаем текущий объект для поддержки цепочки операций.

    def __sub__(self, dish):
        """Перегрузка оператора - для удаления блюда."""
        if dish in self.dishes:
            self.dishes.remove(dish)  # Удаляем блюдо, если оно есть в списке.
            print(f"Блюдо '{dish}' удалено из заказа {self.order_number}")
        else:
            print(f"Блюдо '{dish}' не найдено в заказе {self.order_number}")
        return self  # Возвращаем текущий объект.


# Класс для заказов с доставкой, наследуется от OrderBase
class DeliveryOrder(OrderBase):
    def __init__(self, order_number, delivery_address, delivery_time):
        super().__init__(order_number)  # Инициализируем базовый класс.
        self.delivery_address = delivery_address  # Адрес доставки.
        self.delivery_time = delivery_time  # Время доставки.
        self.dishes = []  # Список блюд в заказе.

    def display_info(self):
        """Выводит информацию о заказе с доставкой."""
        super().display_info()  # Вызываем базовый метод для отображения номера заказа и статуса.
        print(f"Адрес доставки: {self.delivery_address}")
        print(f"Время доставки: {self.delivery_time}")

    def __str__(self):
        """Строковое представление заказа с доставкой."""
        return (f"{super().__str__()}, Адрес доставки: {self.delivery_address}, "
                f"Время доставки: {self.delivery_time}")

    def add_dish(self, dish):
        """Добавляет блюдо в заказ с доставкой."""
        self.dishes.append(dish)  # Добавляем блюдо в список блюд.
        print(f"Блюдо '{dish}' добавлено в заказ с доставкой {self.order_number}")


# Обработчик команд для Linux.
def linux_commands(orders, command):
    # Обработка команды "touch" для создания нового заказа
    if command.startswith("touch"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]  # Получаем номер заказа.
            new_order = Order(order_number)  # Создаем новый заказ.
            orders.append(new_order)  # Добавляем заказ в список.
            print(f"Заказ {order_number} создан командой touch.")
        else:
            print("Ошибка: Использование команды 'touch <номер заказа>'.")

    # Обработка команды "add" для добавления блюда в заказ
    elif command.startswith("add"):
        parts = command.split()
        if len(parts) == 3:
            order_number = parts[1]
            dish = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order + dish  # Используем перегруженный оператор + для добавления блюда.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'add <номер заказа> <блюдо>'.")

    # Обработка команды "status" для изменения статуса заказа
    elif command.startswith("status"):
        parts = command.split()
        if len(parts) == 3:
            order_number = parts[1]
            new_status = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)  # Изменяем статус заказа.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'status <номер заказа> <новый статус>'.")

    # Обработка команды "info" для вывода информации о заказе
    elif command.startswith("info"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()  # Выводим информацию о заказе.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'info <номер заказа>'.")

    # Обработка команды "list" для вывода всех заказов
    elif command.startswith("list"):
        print("Список всех заказов:")
        for order in orders:
            print(order)  # Выводим строковое представление каждого заказа.

    # Обработка команды "total" для вывода общего количества заказов
    elif command.startswith("total"):
        OrderBase.total_orders()  # Вызываем метод вывода общего количества заказов.

    # Обработка команды "str" для вывода строкового представления заказа
    elif command.startswith("str"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            for order in orders:
                if order.order_number == order_number:
                    print(order)  # Выводим строковое представление заказа.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'str <номер заказа>'.")


# Функция справки по командам Linux
def show_linux_help():
    """Вывод справки по командам Linux."""
    print("\n--- Доступные команды Linux ---")
    print("1. 'touch <номер заказа>' - Создать новый заказ с указанным номером.")
    print("2. 'add <номер заказа> <блюдо>' - Добавить блюдо в заказ.")
    print("3. 'status <номер заказа> <новый статус>' - Изменить статус заказа.")
    print("4. 'info <номер заказа>' - Показать информацию о заказе.")
    print("5. 'list' - Показать все заказы.")
    print("6. 'total' - Показать общее количество заказов.")
    print("7. 'str <номер заказа>' - Показать строковое представление заказа.")


# Функция меню для взаимодействия с пользователем
def main_menu():
    orders = []  # Список для хранения всех заказов.
    os_type = os.name  # Определяем тип операционной системы.

    while True:
        # Выводим главное меню для выбора опций.
        print("\n--- Управление заказами ---")
        print("1. Создать заказ")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Показать общее количество заказов")
        print("7. Показать строковое представление заказа")
        if os_type == "posix":  # Если система Linux/Unix.
            print("8. Выполнить команду Linux")
            print("9. Показать справку по командам Linux")
        print("10. Выйти")
        choice = input("Выберите опцию: ")  # Получаем выбор пользователя.

        if choice == '1':
            order_type = input("Введите 'D' для заказа с доставкой или 'O' для обычного заказа: ").upper()
            order_number = input("Введите номер заказа: ")

            if order_type == 'D':  # Если заказ с доставкой.
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(order_number, address, delivery_time)  # Создаем заказ с доставкой.
            else:
                order = Order(order_number)  # Создаем обычный заказ.

            orders.append(order)  # Добавляем заказ в список.
            print(f"Заказ {order_number} создан.")

        elif choice == '2':
            order_number = input("Введите номер заказа: ")
            dish = input("Введите название блюда: ")
            for order in orders:
                if order.order_number == order_number:
                    order + dish  # Используем перегруженный оператор + для добавления блюда.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '3':
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()  # Выводим информацию о заказе.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '4':
            order_number = input("Введите номер заказа: ")
            new_status = input("Введите новый статус: ")
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)  # Изменяем статус заказа.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '5':
            for order in orders:
                print(order)  # Выводим строковое представление всех заказов.

        elif choice == '6':
            OrderBase.total_orders()  # Вызываем метод для вывода общего количества заказов.

        elif choice == '7':
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:
                    print(order)  # Выводим строковое представление заказа.
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '8' and os_type == "posix":
            command = input("Введите команду Linux для выполнения (например, 'touch', 'add', 'status', 'info', 'list', 'total', 'str'): ")
            linux_commands(orders, command)  # Выполняем команду Linux.

        elif choice == '9' and os_type == "posix":
            show_linux_help()  # Показываем справку по командам Linux.

        elif choice == '10':
            print("Выход из программы.")  # Завершаем работу программы.
            break

        else:
            print("Неверный выбор. Попробуйте снова.")  # Если пользователь ввел неверный выбор.


# Запуск программы
if __name__ == "__main__":
    main_menu()  # Вызываем главное меню.