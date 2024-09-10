# Класс, описывающий книгу
class Book:
    def __init__(self, title, author, year, pages):
        # Инициализация параметров книги
        self.title = title          # Название книги
        self.author = author        # Автор книги
        self.year = year            # Год издания
        self.pages = pages          # Количество страниц
        self.dostup = True          # Статус доступности (True, если доступна)
    # Метод для взятия книги
    def borrow_book(self):
        if self.dostup:
            self.dostup = False     # Если книга доступна, она берется, и статус меняется на False
            print(f"Вы взяли книгу: {self.title}")
        else:
            # Если книга уже взята, вывести предупреждение
            print(f"Книга '{self.title}' уже на руках.")
    # Метод для возврата книги
    def return_book(self):
        if not self.dostup:
            self.dostup = True      # Если книга на руках, вернуть и изменить статус на True
            print(f"Вы вернули книгу: {self.title}")
        else:
            # Если книга уже возвращена, вывести предупреждение
            print(f"Книга '{self.title}' уже находится в библиотеке.")
    # Метод для отображения информации о книге
    def display_info(self):
        # Определение статуса книги (доступна или на руках)
        status = "Доступна" if self.dostup else "На руках у пользователя"
        # Возвращение строки с информацией о книге
        return f"'{self.title}' by {self.author} ({self.year}, {self.pages} стр.), статус: {status}"
# Класс для управления библиотекой
class Library:
    def __init__(self):
        # Инициализация пустого списка для хранения книг
        self.books = []

    # Метод для добавления книги в библиотеку
    def add_book(self, book):
        self.books.append(book)     # Добавление книги в список

    # Метод для показа списка книг
    def show_books(self):
        if not self.books:
            # Если список книг пуст, вывести сообщение
            print("Библиотека пуста.")
        else:
            # Перебор книг и их вывод с индексами
            for i, book in enumerate(self.books, 1):
                print(f"{i}. {book.title}")  # Вывод индекса и названия книги
    # Метод для взятия книги по индексу
    def take_book(self, book_index):
        if 0 <= book_index < len(self.books):
            # Если индекс корректен, вызвать метод borrow_book() для книги
            book = self.books[book_index]
            book.borrow_book()
        else:
            # Если индекс некорректен, вывести сообщение
            print("Некорректный индекс книги.")
    # Метод для возврата книги по индексу
    def return_book(self, book_index):
        if 0 <= book_index < len(self.books):
            # Если индекс корректен, вызвать метод return_book() для книги
            book = self.books[book_index]
            book.return_book()
        else:
            # Если индекс некорректен, вывести сообщение
            print("Некорректный индекс книги.")
# Функция для создания новой книги на основе пользовательского ввода
def create_book():
    # Запрос информации о новой книге у пользователя
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = int(input("Введите год издания книги: "))
    pages = int(input("Введите количество страниц книги: "))
    # Возвращение объекта Book с введенными данными
    return Book(title, author, year, pages)
# Функция для отображения меню и управления библиотекой
def menu():
    library = Library()  # Создание экземпляра библиотеки
    while True:
        # Отображение меню
        print("\nМеню:")
        print("1. Взять книгу")
        print("2. Вернуть книгу")
        print("3. Показать информацию о книгах")
        print("4. Добавить новую книгу")
        print("5. Выйти")
        choice = input("Выберите опцию: ")  # Ввод выбора пользователя
        if choice == "1":
            # Показать список книг и предложить выбрать книгу для взятия
            library.show_books()
            if library.books:
                index = int(input("Введите номер книги, которую хотите взять: ")) - 1
                library.take_book(index)
        elif choice == "2":
            # Показать список книг и предложить выбрать книгу для возврата
            library.show_books()
            if library.books:
                index = int(input("Введите номер книги, которую хотите вернуть: ")) - 1
                library.return_book(index)
        elif choice == "3":
            # Показать список книг и их подробную информацию
            library.show_books()
            for book in library.books:
                print(book.display_info())
        elif choice == "4":
            # Добавить новую книгу, запросив данные у пользователя
            new_book = create_book()
            library.add_book(new_book)
            print(f"Книга '{new_book.title}' добавлена в библиотеку.")
        elif choice == "5":
            # Завершить выполнение программы
            print("Выход из программы.")
            break
if __name__ == "__main__":
    menu()  