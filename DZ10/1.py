import os
from abc import ABC, abstractmethod
from typing import List

class OrderBase(ABC):
    total_order_count: int = 0  # Статический атрибут для хранения общего количества заказов

    def __init__(self, order_number: int, status: str = "В процессе"):
        self.order_number: int = order_number
        self.status: str = status
        OrderBase.total_order_count += 1

    @abstractmethod
    def display_info(self) -> None:
        """Абстрактный метод для отображения информации о заказе"""
        pass

    @staticmethod
    def total_orders() -> int:
        """Возвращает общее количество заказов"""
        return OrderBase.total_order_count

    def __str__(self) -> str:
        """Переопределенный метод для строкового представления объекта заказа"""
        return f"Заказ {self.order_number}, Статус: {self.status}"


class Order(OrderBase):
    def __init__(self, order_number: int):
        super().__init__(order_number)
        self.dishes: List[str] = []

    def add_dish(self, dish: str) -> None:
        """Добавить блюдо в заказ"""
        self.dishes.append(dish)
        print(f"Блюдо '{dish}' добавлено в заказ {self.order_number}")

    def change_status(self, status: str) -> None:
        """Изменить статус заказа"""
        self.status = status
        print(f"Статус заказа {self.order_number} изменен на '{self.status}'")

    def display_info(self) -> None:
        """Вывод информации о заказе"""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")

    def __str__(self) -> str:
        return f"{super().__str__()}, Блюда: {', '.join(self.dishes)}"


class DeliveryOrder(OrderBase):
    def __init__(self, order_number: int, delivery_address: str, delivery_time: str):
        super().__init__(order_number)
        self.delivery_address: str = delivery_address
        self.delivery_time: str = delivery_time
        self.dishes: List[str] = []

    def display_info(self) -> None:
        """Вывод информации о заказе с доставкой"""
        print(f"Номер заказа: {self.order_number}")
        print(f"Блюда: {', '.join(self.dishes)}")
        print(f"Статус: {self.status}")
        print(f"Адрес доставки: {self.delivery_address}")
        print(f"Время доставки: {self.delivery_time}")

    def __str__(self) -> str:
        return (f"{super().__str__()}, Адрес доставки: {self.delivery_address}, "
                f"Время доставки: {self.delivery_time}")


# Обработчик команд для Linux
def linux_commands(orders: List[OrderBase], command: str) -> None:
    if command.startswith("touch"):
        parts = command.split()
        if len(parts) == 2:
            order_number = int(parts[1])
            new_order = Order(order_number)
            orders.append(new_order)
            print(f"Заказ {order_number} создан командой touch.")
        else:
            print("Ошибка: Использование команды 'touch <номер заказа>'.")

    elif command.startswith("add"):
        parts = command.split()
        if len(parts) == 3:
            order_number = int(parts[1])
            dish = parts[2]
            for order in orders:
                if order.order_number == order_number:
                    order.add_dish(dish)
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")
        else:
            print("Ошибка: Использование команды 'add <номер заказа> <блюдо>'.")

    elif command.startswith("status"):
        parts = command.split()
        if len(parts) == 3:
            order_number = int(parts[1])
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
            order_number = int(parts[1])
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
        print(f"Общее количество заказов: {OrderBase.total_orders()}")


# Функция справки по командам Linux
def show_linux_help() -> None:
    print("\n--- Доступные команды Linux ---")
    print("1. 'touch <номер заказа>' - Создать новый заказ с указанным номером.")
    print("2. 'add <номер заказа> <блюдо>' - Добавить блюдо в заказ.")
    print("3. 'status <номер заказа> <новый статус>' - Изменить статус заказа.")
    print("4. 'info <номер заказа>' - Показать информацию о заказе.")
    print("5. 'list' - Показать все заказы.")
    print("6. 'total' - Показать общее количество заказов.")


# Функция меню
def main_menu() -> None:
    orders: List[OrderBase] = []
    os_type = os.name

    while True:
        print("\n--- Управление заказами ---")
        print("1. Создать заказ")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Показать общее количество заказов")
        if os_type == "posix":
            print("7. Выполнить команду Linux")
            print("8. Показать справку по командам Linux")
        print("9. Выйти")
        choice = input("Выберите опцию: ")

        if choice == '1':
            order_type = input("Введите 'D' для заказа с доставкой или 'O' для обычного заказа: ").upper()
            order_number = int(input("Введите номер заказа: "))

            if order_type == 'D':
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(order_number, address, delivery_time)
            else:
                order = Order(order_number)

            orders.append(order)
            print(f"Заказ {order_number} создан.")

        elif choice == '2':
            order_number = int(input("Введите номер заказа: "))
            dish = input("Введите название блюда: ")
            for order in orders:
                if order.order_number == order_number:
                    order.add_dish(dish)
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '3':
            order_number = int(input("Введите номер заказа: "))
            for order in orders:
                if order.order_number == order_number:
                    order.display_info()
                    break
            else:
                print(f"Заказ с номером {order_number} не найден.")

        elif choice == '4':
            order_number = int(input("Введите номер заказа: "))
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
            print(f"Общее количество заказов: {OrderBase.total_orders()}")

        elif choice == '7' and os_type == "posix":
            command = input("Введите команду Linux для выполнения (например, 'touch', 'add', 'status', 'info', 'list', 'total'): ")
            linux_commands(orders, command)

        elif choice == '8' and os_type == "posix":
            show_linux_help()

        elif choice == '9':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    main_menu()
