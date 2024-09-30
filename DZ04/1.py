import random
import peewee as pw

# Настройка базы данных
db = pw.SqliteDatabase('restaurant.db')

class BaseModel(pw.Model):
    class Meta:
        database = db

class Dish(BaseModel):
    name = pw.CharField()
    category = pw.CharField()

class Order(BaseModel):
    order_number = pw.IntegerField(unique=True)
    status = pw.CharField(default="Создан")
    address = pw.CharField(null=True)  # Для адресов доставки
    delivery_time = pw.CharField(null=True)  # Для времени доставки

class OrderDish(BaseModel):
    order = pw.ForeignKeyField(Order, backref='dishes')
    dish_name = pw.CharField()  # Теперь сохраняем название блюда

# Создание таблиц в базе данных
db.connect()
db.create_tables([Dish, Order, OrderDish], safe=True)

def generate_buffet():
    categories = {
        "Салаты": ["Цезарь с курицей", "Греческий салат", "Салат из свежих овощей", "Оливье", "Винегрет"],
        "Закуски": ["Канапе с семгой и крем-сыром", "Ассорти сыров", "Ветчина с дыней", "Маринованные грибы", "Рулеты из баклажанов с орехами"],
        "Основные блюда": ["Запеченный лосось", "Курица в соусе терияки", "Говядина в красном вине", "Свиные ребрышки барбекю", "Тушеные овощи с грибами"],
        "Гарниры": ["Картофельное пюре", "Рис с овощами", "Запеченные овощи", "Спагетти с соусом песто", "Кускус с овощами"],
        "Десерты": ["Тирамису", "Шоколадный мусс", "Фруктовый салат", "Чизкейк", "Яблочный штрудель"],
        "Напитки": ["Апельсиновый сок", "Минеральная вода", "Вино (белое и красное)", "Кофе", "Чай"]
    }
    
    # Добавление блюд в базу данных
    for category, items in categories.items():
        for item in items:
            Dish.get_or_create(name=item, category=category)  # Избегает дублирования

def print_buffet():
    print("Текущее меню шведского стола:\n" + "="*30)
    for dish in Dish.select():
        print(f"{dish.category}: {dish.name} - это блюдо обладает уникальным вкусом и отлично подойдет для вашего праздника или обеда.")
    print("="*30)

def add_custom_dish():
    print("Выберите категорию для добавления нового блюда:")
    categories = list(Dish.select(pw.fn.DISTINCT(Dish.category)))  # Уникальные категории
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.category} - категория с множеством интересных вариантов.")
    print(f"{len(categories) + 1}. Создать новую категорию")  # Добавляем возможность создания новой категории

    category_choice = int(input("Введите номер категории или выберите создание новой категории: ")) - 1

    if category_choice == len(categories):  # Если пользователь выбрал создание новой категории
        category_name = input("Введите название новой категории: ")
    else:
        category_name = categories[category_choice].category
    new_dish = input(f"Введите название нового блюда для категории '{category_name}': ")

    # Добавление нового блюда в базу данных
    Dish.create(name=new_dish, category=category_name)
    print(f"Новое блюдо '{new_dish}' было успешно добавлено в категорию '{category_name}'. Теперь ваше меню стало еще разнообразнее и интереснее для ваших гостей и клиентов!")

def choose_dish():
    print("Выберите блюдо из текущего разнообразного и аппетитного меню, которое состоит из лучших предложений для вашего заказа:")
    dishes = list(Dish.select())
    for i, dish in enumerate(dishes, 1):
        print(f"{i}. {dish.category}: {dish.name} - это превосходное блюдо, которое порадует любого гурмана и станет настоящей изюминкой вашего заказа!")

    choice = input("Введите номер или название блюда, которое вы хотите добавить в заказ: ")
    
    # Проверка, является ли ввод числом или строкой
    if choice.isdigit():
        choice = int(choice) - 1
        if 0 <= choice < len(dishes):
            chosen_dish = dishes[choice]
            print(f"Вы выбрали великолепное блюдо '{chosen_dish.name}' из категории '{chosen_dish.category}'. Отличный выбор!")
            return chosen_dish
        else:
            print("Неверный номер блюда.")
            return None
    else:
        # Поиск блюда по названию
        chosen_dish = Dish.get_or_none(Dish.name == choice)
        if chosen_dish:
            print(f"Вы выбрали великолепное блюдо '{chosen_dish.name}' из категории '{chosen_dish.category}'. Отличный выбор!")
            return chosen_dish
        else:
            print("Блюдо с таким названием не найдено.")
            return None

def manage_orders():
    while True:
        print("\nМеню управления заказами:")
        print("1. Создать новый заказ (обычный заказ или заказ с доставкой)")
        print("2. Добавить блюдо в существующий заказ")
        print("3. Показать информацию о заказе")
        print("4. Изменить статус заказа")
        print("5. Показать все заказы")
        print("6. Удалить завершённый заказ")
        print("7. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            order_type = input("Создать обычный заказ или заказ с доставкой? (обычный/доставка): ").strip().lower()
            order_number = Order.select().count() + 1
            if order_type == "обычный":
                order = Order.create(order_number=order_number)
            else:
                address = input("Введите адрес доставки: ")
                delivery_time = input("Введите время доставки: ")
                order = Order.create(order_number=order_number, address=address, delivery_time=delivery_time)
            print(f"Заказ #{order.order_number} был успешно создан.")

        elif choice == "2":
            order_number = int(input("Введите номер заказа для добавления блюда: "))
            order = Order.get_or_none(Order.order_number == order_number)
            if order:
                dish = choose_dish()
                if dish:  # Проверка на случай, если dish равно None
                    OrderDish.create(order=order, dish_name=dish.name)  # Сохраняем название блюда
                    print(f"Блюдо '{dish.name}' добавлено в заказ #{order_number}.")
            else:
                print(f"Заказ с номером #{order_number} не найден.")

        elif choice == "3":
            order_number = int(input("Введите номер заказа для отображения информации: "))
            order = Order.get_or_none(Order.order_number == order_number)
            if order:
                print(f"\nЗаказ #{order.order_number} (Статус: {order.status}):")
                if order.address:
                    print(f"Адрес доставки: {order.address}")
                    print(f"Время доставки: {order.delivery_time}")
                print("Список блюд в заказе:")
                for order_dish in order.dishes:
                    print(f" - {order_dish.dish_name}")  # Выводим название блюда
            else:
                print(f"Заказ с номером #{order_number} не найден.")

        elif choice == "4":
            order_number = int(input("Введите номер заказа для изменения статуса: "))
            order = Order.get_or_none(Order.order_number == order_number)
            if order:
                if order.address:
                    new_status = "В пути" if order.status == "Создан" else "Доставлен"
                    order.status = new_status
                else:
                    new_status = input("Введите новый статус для заказа: ")
                    order.status = new_status
                order.save()
                print(f"Статус заказа #{order_number} был успешно обновлён до '{order.status}'.")
            else:
                print(f"Заказ с номером #{order_number} не найден.")

        elif choice == "5":
            print("\nВсе заказы:")
            for order in Order.select():
                print(f"Заказ #{order.order_number} (Статус: {order.status})")
                for order_dish in order.dishes:
                    print(f" - {order_dish.dish_name}")  # Выводим название блюда

        elif choice == "6":
            order_number = int(input("Введите номер заказа для удаления: "))
            order = Order.get_or_none(Order.order_number == order_number)
            if order:
                order.delete_instance(recursive=True)
                print(f"Заказ #{order_number} был успешно удалён.")
            else:
                print(f"Заказ с номером #{order_number} не найден.")

        elif choice == "7":
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

def main_menu():
    generate_buffet()
    while True:
        print("\nГлавное меню:")
        print("1. Показать текущее меню шведского стола")
        print("2. Добавить новое блюдо в меню")
        print("3. Управление заказами")
        print("4. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            print_buffet()

        elif choice == "2":
            add_custom_dish()

        elif choice == "3":
            manage_orders()

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

if __name__ == "__main__":
    main_menu()