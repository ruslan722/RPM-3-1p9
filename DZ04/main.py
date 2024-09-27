import random

class Order:
    order_counter = 1  # Счетчик для уникальных номеров заказов
    
    def __init__(self, dishes=None, status="Создан"):
        self.order_number = Order.order_counter
        Order.order_counter += 1
        self.dishes = dishes if dishes else []
        self.status = status

    def add_dish(self, dish):
        self.dishes.append(dish)

    def show_order(self):
        print(f"Заказ #{self.order_number} (Статус: {self.status}):")
        for dish in self.dishes:
            print(f" - {dish}")
        print()

    def update_status(self, new_status):
        self.status = new_status

class DeliveryOrder(Order):
    def __init__(self, address, delivery_time, dishes=None, status="Создан"):
        super().__init__(dishes, status)
        self.address = address
        self.delivery_time = delivery_time

    def update_delivery_status(self):
        if self.status == "Создан":
            self.status = "В пути"
        elif self.status == "В пути":
            self.status = "Доставлен"

    def show_order(self):
        super().show_order()
        print(f"Адрес доставки: {self.address}")
        print(f"Время доставки: {self.delivery_time}\n")

def generate_buffet():
    salads = ["Цезарь с курицей", "Греческий салат", "Салат из свежих овощей", "Оливье", "Винегрет"]
    appetizers = ["Канапе с семгой и крем-сыром", "Ассорти сыров", "Ветчина с дыней", "Маринованные грибы", "Рулеты из баклажанов с орехами"]
    main_courses = ["Запеченный лосось", "Курица в соусе терияки", "Говядина в красном вине", "Свиные ребрышки барбекю", "Тушеные овощи с грибами"]
    sides = ["Картофельное пюре", "Рис с овощами", "Запеченные овощи", "Спагетти с соусом песто", "Кускус с овощами"]
    desserts = ["Тирамису", "Шоколадный мусс", "Фруктовый салат", "Чизкейк", "Яблочный штрудель"]
    drinks = ["Апельсиновый сок", "Минеральная вода", "Вино (белое и красное)", "Кофе", "Чай"]

    categories = {
        "Салаты": salads,
        "Закуски": appetizers,
        "Основные блюда": main_courses,
        "Гарниры": sides,
        "Десерты": desserts,
        "Напитки": drinks
    }
    
    buffet = {category: random.sample(items, 3) for category, items in categories.items()}
    return buffet, categories

def print_buffet(buffet):
    print("Текущее меню шведского стола:")
    for category, items in buffet.items():
        print(f"{category}:")
        for item in items:
            print(f" - {item}")
        print()

def add_custom_dish(buffet, categories):
    print("Выберите категорию для добавления блюда:")
    for i, category in enumerate(categories.keys(), 1):
        print(f"{i}. {category}")
    category_choice = int(input("Введите номер категории: ")) - 1
    category_name = list(categories.keys())[category_choice]
    new_dish = input(f"Введите название нового блюда для категории '{category_name}': ")
    categories[category_name].append(new_dish)
    buffet[category_name] = random.sample(categories[category_name], 3)
    print("\nОбновленное меню шведского стола:")
    print_buffet(buffet)

def choose_dish(buffet):
    print("Выберите блюдо из текущего меню:")
    for i, (category, items) in enumerate(buffet.items(), 1):
        print(f"{i}. {category}:")
        for j, item in enumerate(items, 1):
            print(f"  {j}. {item}")
    print()

    category_choice = int(input("Введите номер категории: ")) - 1
    category_name = list(buffet.keys())[category_choice]
    
    dish_choice = int(input(f"Введите номер блюда из категории '{category_name}': ")) - 1
    chosen_dish = buffet[category_name][dish_choice]
    
    print(f"Вы выбрали: {chosen_dish}")
    return chosen_dish

def manage_orders(orders, buffet):
    while True:
        print("\nМеню управления заказами:")
        print("1. Создать заказ (обычный или доставка)")
        print("2. Добавить блюдо в заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Удалить завершенный заказ")
        print("7. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            order_type = input("Создать обычный заказ или заказ с доставкой? (обычный/доставка): ").strip().lower()
            if order_type == "обычный":
                order = Order()
            else:
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = DeliveryOrder(address, delivery_time)
            orders.append(order)
            print(f"Заказ #{order.order_number} создан.")

        elif choice == "2":
            order_number = int(input("Введите номер заказа для добавления блюда: "))
            order = next((o for o in orders if o.order_number == order_number), None)
            if order:
                dish = choose_dish(buffet)
                order.add_dish(dish)
                print(f"Блюдо '{dish}' добавлено в заказ #{order_number}.")
            else:
                print(f"Заказ #{order_number} не найден.")

        elif choice == "3":
            order_number = int(input("Введите номер заказа для отображения информации: "))
            order = next((o for o in orders if o.order_number == order_number), None)
            if order:
                order.show_order()
            else:
                print(f"Заказ #{order_number} не найден.")

        elif choice == "4":
            order_number = int(input("Введите номер заказа для изменения статуса: "))
            order = next((o for o in orders if o.order_number == order_number), None)
            if order:
                if isinstance(order, DeliveryOrder):
                    order.update_delivery_status()
                else:
                    new_status = input("Введите новый статус заказа: ")
                    order.update_status(new_status)
                print(f"Статус заказа #{order_number} обновлен.")
            else:
                print(f"Заказ #{order_number} не найден.")

        elif choice == "5":
            print("\nВсе заказы:")
            for order in orders:
                order.show_order()

        elif choice == "6":
            order_number = int(input("Введите номер заказа для удаления: "))
            orders = [o for o in orders if o.order_number != order_number]
            print(f"Заказ #{order_number} удален.")

        elif choice == "7":
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

def main_menu():
    buffet, categories = generate_buffet()
    orders = []  # Список для хранения заказов

    while True:
        print("\nГлавное меню:")
        print("1. Показать текущее меню шведского стола")
        print("2. Добавить блюдо в меню шведского стола")
        print("3. Управление заказами")
        print("4. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            print_buffet(buffet)

        elif choice == "2":
            add_custom_dish(buffet, categories)

        elif choice == "3":
            manage_orders(orders, buffet)

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

if __name__ == "__main__":
    main_menu()
