import os
from abc import ABC, abstractmethod

class OrderBase(ABC):
    total_order_count = 0  # Статический атрибут для хранения общего количества заказов

    def __init__(self, order_number):
        self.order_number = order_number
        self.status = "В процессе"
        OrderBase.total_order_count += 1

    @abstractmethod
    def display_info(self):
        pass

    @staticmethod
    def total_orders():
        """Вывести общее количество заказов"""
        print(f"Общее количество заказов: {OrderBase.total_order_count}")

    def __str__(self):
        """Строковое представление объекта заказа"""
        return f"Заказ {self.order_number}, Статус: {self.status}"


class Order(OrderBase):
    def __init__(self, order_number):
        super().__init__(order_number)
        self.dishes = []

    def display_info(self):
        """Вывод информации о заказе"""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")

    def add_dish(self, dish):
        """Добавить блюдо в заказ"""
        self.dishes.append(dish)
        print(f"Блюдо '{dish}' добавлено в заказ {self.order_number}")

    def change_status(self, status):
        """Изменить статус заказа"""
        self.status = status
        print(f"Статус заказа {self.order_number} изменен на '{self.status}'")

    def __str__(self):
        return f"{super().__str__()}, Блюда: {', '.join(self.dishes)}"

    def __add__(self, dish):
        self.add_dish(dish)
        return self

    def __sub__(self, dish):
        if dish in self.dishes:
            self.dishes.remove(dish)
            print(f"Блюдо '{dish}' удалено из заказа {self.order_number}")
        else:
            print(f"Блюдо '{dish}' не найдено в заказе {self.order_number}")
        return self


class DeliveryOrder(OrderBase):
    def __init__(self, order_number, delivery_address, delivery_time):
        super().__init__(order_number)
        self.delivery_address = delivery_address
        self.delivery_time = delivery_time
        self.dishes = []

    def display_info(self):
        """Вывод информации о заказе с доставкой"""
        super().display_info()
        print(f"Адрес доставки: {self.delivery_address}")
        print(f"Время доставки: {self.delivery_time}")

    def __str__(self):
        return (f"{super().__str__()}, Адрес доставки: {self.delivery_address}, "
                f"Время доставки: {self.delivery_time}")

    def add_dish(self, dish):
        """Добавить блюдо в заказ"""
        self.dishes.append(dish)
        print(f"Блюдо '{dish}' добавлено в заказ с доставкой {self.order_number}")


# Обработчик команд для Linux
def linux_commands(orders, command):
    if command.startswith("touch"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            new_order = Order(order_number)
            orders.append(new_order)
            print(f"Заказ {order_number} создан командой touch.")
        else:
            print("Ошибка: Использование команды 'touch <номер заказа>'.")

    elif command.startswith("add"):
        parts = command.split()
        if len(parts) == 3:
            order_number = parts[1]
            dish = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order + dish  # Используем перегруженный оператор +
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'add <номер заказа> <блюдо>'.")

    elif command.startswith("status"):
        parts = command.split()
        if len(parts) == 3:
            order_number = parts[1]
            new_status = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'status <номер заказа> <новый статус>'.")

    elif command.startswith("info"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'info <номер заказа>'.")

    elif command.startswith("list"):
        print("Список всех заказов:")
        for order in orders:
            print(order)

    elif command.startswith("total"):
        OrderBase.total_orders()

    elif command.startswith("str"):
        parts = command.split()
        if len(parts) == 2:
            order_number = parts[1]
            for order in orders:
                if order.order_number == order_number:
                    print(order)
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'str <номер заказа>'.")


# Функция справки по командам Linux
def show_linux_help():
    print("\n--- Доступные команды Linux ---")
    print("1. 'touch <номер заказа>' - Создать новый заказ с указанным номером.")
    print("2. 'add <номер заказа> <блюдо>' - Добавить блюдо в заказ.")
    print("3. 'status <номер заказа> <новый статус>' - Изменить статус заказа.")
    print("4. 'info <номер заказа>' - Показать информацию о заказе.")
    print("5. 'list' - Показать все заказы.")
    print("6. 'total' - Показать общее количество заказов.")
    print("7. 'str <номер заказа>' - Показать строковое представление заказа.")


# Функция меню
def main_menu():
    orders = []
    os_type = os.name

    while True:
        print("\n--- Управление заказами ---")
        print("1. Создать заказ")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Показать общее количество заказов")
        print("7. Показать строковое представление заказа")
        if os_type == "posix":
            print("8. Выполнить команду Linux")
            print("9. Показать справку по командам Linux")
        print("10. Выйти")
        choice = input("Выберите опцию: ")

        if choice == '1':
            order_type = input("Введите 'D' для заказа с доставкой или 'O' для обычного заказа: ").upper()
            order_number = input("Введите номер заказа: ")

            if order_type == 'D':
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(order_number, address, delivery_time)
            else:
                order = Order(order_number)

            orders.append(order)
            print(f"Заказ {order_number} создан.")

        elif choice == '2':
            order_number = input("Введите номер заказа: ")
            dish = input("Введите название блюда: ")
            for order in orders:
                if order.order_number == order_number:
                    order + dish  # Используем перегруженный оператор +
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '3':
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '4':
            order_number = input("Введите номер заказа: ")
            new_status = input("Введите новый статус: ")
            for order in orders:
                if order.order_number == order_number:
                    order.change_status(new_status)
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '5':
            for order in orders:
                print(order)

        elif choice == '6':
            OrderBase.total_orders()

        elif choice == '7':
            order_number = input("Введите номер заказа: ")
            for order in orders:
                if order.order_number == order_number:
                    print(order)  # Выводим строковое представление заказа
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '8' and os_type == "posix":
            command = input("Введите команду Linux для выполнения (например, 'touch', 'add', 'status', 'info', 'list', 'total', 'str'): ")
            linux_commands(orders, command)

        elif choice == '9' and os_type == "posix":
            show_linux_help()

        elif choice == '10':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    main_menu()