import os  # Импортируем модуль os, чтобы использовать его для проверки операционной системы

# Класс для работы с заказами
class Order:
    total_order_count = 0  # Статический атрибут для хранения общего количества заказов

    def __init__(self, order_number):
        # Конструктор класса Order, инициализирует заказ
        self.order_number = order_number  # Номер заказа
        self.dishes = []  # Список блюд в заказе
        self.status = "В процессе"  # Начальный статус заказа
        Order.total_order_count += 1  # Увеличиваем общее количество заказов на 1

    def display_info(self):
        """Вывод информации о заказе"""
        # Метод выводит информацию о заказе: номер, блюда, статус
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")

    def add_dish(self, dish):
        """Добавить блюдо в заказ"""
        # Метод добавляет блюдо в список блюд заказа
        self.dishes.append(dish)  # Добавляем блюдо в список
        print(f"Блюдо '{dish}' добавлено в заказ {self.order_number}")  # Выводим сообщение о добавлении

    def change_status(self, status):
        """Изменить статус заказа"""
        # Метод изменяет статус заказа
        self.status = status  # Обновляем статус заказа
        print(f"Статус заказа {self.order_number} изменен на '{self.status}'")  # Выводим сообщение о новом статусе

    @staticmethod
    def total_orders():
        """Вывести общее количество заказов"""
        # Статический метод выводит количество всех заказов
        print(f"Общее количество заказов: {Order.total_order_count}")  # Выводим общее количество заказов

    def __str__(self):
        """Строковое представление объекта заказа"""
        # Метод возвращает строковое представление заказа (для удобного вывода)
        return f"Заказ {self.order_number}: Блюда - {', '.join(self.dishes)}, Статус - {self.status}"


# Класс для работы с заказами на доставку, наследуется от Order
class DeliveryOrder(Order):
    def __init__(self, order_number, delivery_address, delivery_time):
        # Конструктор класса DeliveryOrder, инициализирует заказ с доставкой
        super().__init__(order_number)  # Вызываем конструктор базового класса Order
        self.delivery_address = delivery_address  # Адрес доставки
        self.delivery_time = delivery_time  # Время доставки

    def display_info(self):
        """Вывод информации о заказе с доставкой"""
        # Метод выводит информацию о заказе с доставкой, включая стандартные поля заказа и поля доставки
        super().display_info()  # Вызываем метод display_info() из базового класса
        print(f"Адрес доставки: {self.delivery_address}")  # Выводим адрес доставки
        print(f"Время доставки: {self.delivery_time}")  # Выводим время доставки

    def __str__(self):
        """Строковое представление объекта заказа с доставкой"""
        # Метод возвращает строковое представление заказа с доставкой
        return (f"Заказ {self.order_number}: Блюда - {', '.join(self.dishes)}, "
                f"Статус - {self.status}, Адрес доставки - {self.delivery_address}, "
                f"Время доставки - {self.delivery_time}")


# Функция для выполнения команд в Linux-стиле (для пользователей Linux)
def linux_commands(orders, command):
    if command.startswith("touch"):
        # Команда "touch" создает новый заказ
        parts = command.split()  # Разделяем команду на части
        if len(parts) == 2:
            order_number = parts[1]  # Извлекаем номер заказа
            new_order = Order(order_number)  # Создаем новый заказ
            orders.append(new_order)  # Добавляем заказ в список заказов
            print(f"Заказ {order_number} создан командой touch.")  # Выводим подтверждение создания заказа
        else:
            print("Ошибка: Использование команды 'touch <номер заказа>'.")

    elif command.startswith("add"):
        # Команда "add" добавляет блюдо в заказ
        parts = command.split()  # Разделяем команду на части
        if len(parts) == 3:
            order_number = parts[1]  # Извлекаем номер заказа
            dish = parts[2]  # Извлекаем название блюда
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    order.add_dish(dish)  # Добавляем блюдо в заказ
                    print(f"Блюдо '{dish}' добавлено в заказ {order_number} командой add.")
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'add <номер заказа> <блюдо>'.")

    elif command.startswith("status"):
        # Команда "status" изменяет статус заказа
        parts = command.split()  # Разделяем команду на части
        if len(parts) == 3:
            order_number = parts[1]  # Извлекаем номер заказа
            new_status = parts[2]  # Извлекаем новый статус
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    order.change_status(new_status)  # Меняем статус заказа
                    print(f"Статус заказа {order_number} изменен на '{new_status}' командой status.")
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'status <номер заказа> <новый статус>'.")

    elif command.startswith("info"):
        # Команда "info" выводит информацию о заказе
        parts = command.split()  # Разделяем команду на части
        if len(parts) == 2:
            order_number = parts[1]  # Извлекаем номер заказа
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    order.display_info()  # Выводим информацию о заказе
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'info <номер заказа>'.")

    elif command.startswith("list"):
        # Команда "list" выводит все заказы
        print("Список всех заказов:")
        for order in orders:
            print(order)  # Выводим строковое представление каждого заказа

    elif command.startswith("total"):
        # Команда "total" выводит общее количество заказов
        Order.total_orders()  # Вызываем статический метод для вывода общего количества заказов

    elif command.startswith("str"):
        # Команда "str" выводит строковое представление заказа
        parts = command.split()  # Разделяем команду на части
        if len(parts) == 2:
            order_number = parts[1]  # Извлекаем номер заказа
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    print(order)  # Выводим строковое представление заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'str <номер заказа>'.")


# Функция справки по командам Linux
def show_linux_help():
    # Выводим список доступных команд для пользователей Linux
    print("\n--- Доступные команды Linux ---")
    print("1. 'touch <номер заказа>' - Создать новый заказ с указанным номером.")
    print("2. 'add <номер заказа> <блюдо>' - Добавить блюдо в заказ.")
    print("3. 'status <номер заказа> <новый статус>' - Изменить статус заказа.")
    print("4. 'info <номер заказа>' - Показать информацию о заказе.")
    print("5. 'list' - Показать все заказы.")
    print("6. 'total' - Показать общее количество заказов.")
    print("7. 'str <номер заказа>' - Показать строковое представление заказа.")


# Основная функция меню
def main_menu():
    orders = []  # Список всех заказов
    os_type = os.name  # Определяем тип операционной системы

    while True:
        # Основное меню управления заказами
        print("\n--- Управление заказами ---")
        print("1. Создать заказ")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Показать общее количество заказов")
        print("7. Показать строковое представление заказа")
        if os_type == "posix":  # Проверяем, если это Linux
            print("8. Выполнить команду Linux")
            print("9. Показать справку по командам Linux")
        print("10. Выйти")
        choice = input("Выберите опцию: ")

        if choice == '1':
            # Создание нового заказа
            order_type = input("Введите 'D' для заказа с доставкой или 'O' для обычного заказа: ").upper()
            order_number = input("Введите номер заказа: ")

            if order_type == 'D':
                # Если выбран заказ с доставкой
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(order_number, address, delivery_time)  # Создаем заказ с доставкой
            else:
                order = Order(order_number)  # Создаем обычный заказ

            orders.append(order)  # Добавляем заказ в список заказов
            print(f"Заказ {order_number} создан.")

        elif choice == '2':
            # Добавление блюда в заказ
            order_number = input("Введите номер заказа: ")
            dish = input("Введите название блюда: ")
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    order.add_dish(dish)  # Добавляем блюдо в заказ
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '3':
            # Показ информации о заказе
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    order.display_info()  # Выводим информацию о заказе
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '4':
            # Изменение статуса заказа
            order_number = input("Введите номер заказа: ")
            new_status = input("Введите новый статус: ")
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    order.change_status(new_status)  # Меняем статус заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '5':
            # Показ всех заказов
            for order in orders:
                print(order)  # Выводим строковое представление каждого заказа

        elif choice == '6':
            # Показ общего количества заказов
            Order.total_orders()  # Вызываем статический метод для показа общего количества заказов

        elif choice == '7':
            # Показ строкового представления заказа
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:  # Находим заказ по номеру
                    print(order)  # Выводим строковое представление заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '8' and os_type == "posix":
            # Выполнение команды Linux (доступно только на Linux-системах)
            command = input("Введите команду Linux для выполнения (например, 'touch', 'add', 'status', 'info', 'list', 'total', 'str'): ")
            linux_commands(orders, command)

        elif choice == '9' and os_type == "posix":
            # Показ справки по командам Linux
            show_linux_help()

        elif choice == '10':
            # Выход из программы
            print("Выход из программы.")
            break

        else:
            # Неверный выбор
            print("Неверный выбор. Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    main_menu()  # Вызываем главное меню программы
