import os  # Модуль os используется для определения операционной системы, чтобы различать поведение для Linux (posix).

# Класс Order представляет заказ
class Order:
    total_order_count = 0  # Статический атрибут для хранения общего количества заказов
    
    # Конструктор класса Order
    def __init__(self, order_number):
        self.order_number = order_number  # Номер заказа
        self.dishes = []  # Список блюд в заказе
        self.status = "В процессе"  # Статус заказа
        Order.total_order_count += 1  # Увеличиваем общее количество заказов при создании нового
    
    # Метод для вывода информации о заказе
    def display_info(self):
        """Вывод информации о заказе"""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")

    # Метод для добавления блюда в заказ
    def add_dish(self, dish):
        """Добавить блюдо в заказ"""
        self.dishes.append(dish)
        print(f"Блюдо '{dish}' добавлено в заказ {self.order_number}")

    # Метод для изменения статуса заказа
    def change_status(self, status):
        """Изменить статус заказа"""
        self.status = status
        print(f"Статус заказа {self.order_number} изменен на '{self.status}'")

    # Статический метод для вывода общего количества заказов
    @staticmethod
    def total_orders():
        """Вывести общее количество заказов"""
        print(f"Общее количество заказов: {Order.total_order_count}")

    # Метод для строкового представления заказа
    def __str__(self):
        """Строковое представление объекта заказа"""
        return f"Заказ {self.order_number}: Блюда - {', '.join(self.dishes)}, Статус - {self.status}"

    # Перегрузка оператора + для добавления блюда в заказ
    def __add__(self, dish):
        """Перегрузка оператора + для добавления блюда"""
        self.add_dish(dish)  # Используем метод add_dish для добавления блюда
        return self  # Возвращаем текущий объект заказа для поддержки цепочки операций

    # Перегрузка оператора - для удаления блюда из заказа
    def __sub__(self, dish):
        """Перегрузка оператора - для удаления блюда"""
        if dish in self.dishes:  # Если блюдо есть в списке заказов
            self.dishes.remove(dish)  # Удаляем его
            print(f"Блюдо '{dish}' удалено из заказа {self.order_number}")
        else:
            print(f"Блюдо '{dish}' не найдено в заказе {self.order_number}")
        return self  # Возвращаем текущий объект для поддержки цепочки операций


# Класс DeliveryOrder, который наследуется от Order, представляет заказ с доставкой
class DeliveryOrder(Order):
    def __init__(self, order_number, delivery_address, delivery_time):
        super().__init__(order_number)  # Вызов конструктора родительского класса Order
        self.delivery_address = delivery_address  # Адрес доставки
        self.delivery_time = delivery_time  # Время доставки

    # Переопределение метода для вывода информации о заказе с доставкой
    def display_info(self):
        """Вывод информации о заказе с доставкой"""
        super().display_info()  # Вызов метода display_info из класса Order
        print(f"Адрес доставки: {self.delivery_address}")
        print(f"Время доставки: {self.delivery_time}")

    # Переопределение строкового представления заказа с доставкой
    def __str__(self):
        """Строковое представление объекта заказа с доставкой"""
        return (f"Заказ {self.order_number}: Блюда - {', '.join(self.dishes)}, "
                f"Статус - {self.status}, Адрес доставки - {self.delivery_address}, "
                f"Время доставки - {self.delivery_time}")


# Обработчик команд для Linux, принимающий список заказов и команду
def linux_commands(orders, command):
    # Команда для создания нового заказа
    if command.startswith("touch"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            new_order = Order(order_number)  # Создание нового заказа
            orders.append(new_order)  # Добавление заказа в список заказов
            print(f"Заказ {order_number} создан командой touch.")
        else:
            print("Ошибка: Использование команды 'touch <номер заказа>'.")

    # Команда для добавления блюда в заказ
    elif command.startswith("add"):
        parts = command.split()
        if len(parts) == 3:
            order_number = parts[1]
            dish = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order + dish  # Используем перегруженный оператор + для добавления блюда
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'add <номер заказа> <блюдо>'.")

    # Команда для изменения статуса заказа
    elif command.startswith("status"):
        parts = command.split()
        if len(parts) == 3:
            order_number = parts[1]
            new_status = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)  # Изменяем статус заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'status <номер заказа> <новый статус>'.")

    # Команда для отображения информации о заказе
    elif command.startswith("info"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()  # Отображаем информацию о заказе
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'info <номер заказа>'.")

    # Команда для отображения списка всех заказов
    elif command.startswith("list"):
        print("Список всех заказов:")
        for order in orders:
            print(order)

    # Команда для отображения общего количества заказов
    elif command.startswith("total"):
        Order.total_orders()  # Вызов статического метода для отображения количества заказов

    # Команда для отображения строкового представления заказа
    elif command.startswith("str"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            for order in orders:
                if order.order_number == order_number:
                    print(order)  # Выводим строковое представление заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'str <номер заказа>'.")


# Функция для отображения справки по командам Linux
def show_linux_help():
    print("\n--- Доступные команды Linux ---")
    print("1. 'touch <номер заказа>' - Создать новый заказ с указанным номером.")
    print("2. 'add <номер заказа> <блюдо>' - Добавить блюдо в заказ.")
    print("3. 'status <номер заказа> <новый статус>' - Изменить статус заказа.")
    print("4. 'info <номер заказа>' - Показать информацию о заказе.")
    print("5. 'list' - Показать все заказы.")
    print("6. 'total' - Показать общее количество заказов.")
    print("7. 'str <номер заказа>' - Показать строковое представление заказа.")


# Функция главного меню для работы с заказами
def main_menu():
    orders = []  # Список для хранения всех заказов
    os_type = os.name  # Определяем тип операционной системы

    while True:
        # Вывод главного меню
        print("\n--- Управление заказами ---")
        print("1. Создать заказ")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Показать общее количество заказов")
        print("7. Показать строковое представление заказа")
        if os_type == "posix":  # Если операционная система Linux (posix)
            print("8. Выполнить команду Linux")
            print("9. Показать справку по командам Linux")
        print("10. Выйти")
        choice = input("Выберите опцию: ")

        # Обработка выбора пользователя
        if choice == '1':
            # Создание заказа или заказа с доставкой
            order_type = input("Введите 'D' для заказа с доставкой или 'O' для обычного заказа: ").upper()
            order_number = input("Введите номер заказа: ")

            if order_type == 'D':  # Если заказ с доставкой
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(order_number, address, delivery_time)  # Создание заказа с доставкой
            else:
                order = Order(order_number)  # Создание обычного заказа

            orders.append(order)  # Добавление заказа в список
            print(f"Заказ {order_number} создан.")

        elif choice == '2':
            # Добавление блюда в заказ
            order_number = input("Введите номер заказа: ")
            dish = input("Введите название блюда: ")
            for order in orders:
                if order.order_number == order_number:
                    order + dish  # Используем перегруженный оператор + для добавления блюда
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '3':
            # Показ информации о заказе
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()  # Вывод информации о заказе
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '4':
            # Изменение статуса заказа
            order_number = input("Введите номер заказа: ")
            new_status = input("Введите новый статус: ")
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)  # Изменение статуса заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '5':
            # Показ всех заказов
            for order in orders:
                print(order)

        elif choice == '6':
            # Показ общего количества заказов
            Order.total_orders()

        elif choice == '7':
            # Показ строкового представления заказа
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:
                    print(order)  # Вывод строкового представления заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '8' and os_type == "posix":
            # Выполнение команды Linux
            command = input("Введите команду Linux для выполнения (например, 'touch', 'add', 'status', 'info', 'list', 'total', 'str'): ")
            linux_commands(orders, command)

        elif choice == '9' and os_type == "posix":
            # Показ справки по командам Linux
            show_linux_help()

        elif choice == '10':
            # Выход из программы
            print("Выход из программы.")
            break


# Запуск программы
if __name__ == "__main__":
    main_menu()  # Запуск главного меню