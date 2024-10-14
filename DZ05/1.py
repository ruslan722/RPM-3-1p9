import random  # Импортируем модуль random для генерации случайных значений

class Book:
    # Конструктор класса Book. Инициализирует атрибуты книги.
    def __init__(self, title, author, year, pages, available=None):
        self.title = title  # Название книги
        self.author = author  # Автор книги
        self.year = year  # Год издания книги
        self.pages = pages  # Количество страниц в книге
        self.available = available if available is not None else random.choice([True, False])  # Доступность книги (случайно выбирается, если не указано)
        self.reviews = []  # Пустой список для хранения отзывов

    # Метод для отображения информации о книге
    def display_info(self):
        availability = "доступна" if self.available else "недоступна"  # Устанавливаем строку доступности
        # Выводим информацию о книге
        print(f"\nНазвание: {self.title}\nАвтор: {self.author}\nГод издания: {self.year}\nСтраниц: {self.pages}\nСтатус: {availability}\n")
        self.display_reviews()  # Выводим все отзывы о книге

    # Метод для "взятия" книги
    def take_book(self):
        if self.available:  # Проверяем доступность книги
            self.available = False  # Меняем статус на "недоступна"
            print(f"\nВы взяли книгу: {self.title}\n")  # Уведомляем пользователя о взятии книги
        else:
            print(f"\nКнига '{self.title}' сейчас недоступна.\n")  # Сообщаем, что книга недоступна

    # Метод для "возврата" книги
    def return_book(self):
        if not self.available:  # Если книга недоступна, значит она взята
            self.available = True  # Меняем статус на "доступна"
            print(f"\nКнига '{self.title}' успешно возвращена в библиотеку.\n")  # Сообщаем о возврате книги
        else:
            print(f"\nКнига '{self.title}' уже была доступна.\n")  # Если книга уже доступна, выводим сообщение

    # Метод для добавления отзыва
    def add_review(self, review):
        self.reviews.append(review)  # Добавляем отзыв в список
        print(f"\nВаш отзыв добавлен для книги '{self.title}'.\n")  # Сообщаем о добавлении отзыва

    # Метод для отображения всех отзывов
    def display_reviews(self):
        if self.reviews:  # Если есть отзывы
            print("Отзывы:")  # Выводим заголовок для отзывов
            for review in self.reviews:  # Проходим по каждому отзыву
                print(f"- {review}")  # Выводим каждый отзыв
        else:
            print("Отзывов пока нет. Будьте первым!")  # Если отзывов нет, выводим соответствующее сообщение

    # Статический метод для вывода случайного отзыва
    @staticmethod
    def display_random_review():
        reviews = [
            "Эта книга меня впечатлила!",
            "Отличное произведение, обязательно прочтите.",
            "Немного скучновато, но достойно внимания.",
            "Эта книга затянула меня с первой страницы!",
            "Интересная, но с сложным сюжетом. Советую."
        ]  # Список готовых отзывов
        print(f"Отзыв: {random.choice(reviews)}\n")  # Выбираем и выводим случайный отзыв


class DigitalBook(Book):
    # Конструктор класса DigitalBook. Добавляем новый атрибут - формат файла
    def __init__(self, title, author, year, pages, file_format, available=None):
        super().__init__(title, author, year, pages, available)  # Инициализируем родительский класс Book
        self.file_format = file_format  # Дополнительный атрибут: формат файла

    # Переопределение метода display_info для вывода формата файла
    def display_info(self):
        super().display_info()  # Вызываем метод отображения информации из класса Book
        print(f"Формат файла: {self.file_format}\n")  # Добавляем информацию о формате файла

    # Метод для скачивания цифровой книги
    def download_book(self):
        if self.available:  # Проверяем доступность цифровой книги
            print(f"\nВы скачали цифровую книгу: {self.title} в формате {self.file_format}.\n")  # Сообщаем о скачивании
        else:
            print(f"\nЦифровая книга '{self.title}' недоступна для скачивания.\n")  # Если книга недоступна, выводим сообщение


class Library:
    # Конструктор библиотеки. Инициализирует список книг и загружает несколько начальных книг
    def __init__(self):
        self.books = []  # Список для хранения книг
        self.load_initial_books()  # Загружаем несколько книг по умолчанию

    # Метод для добавления книги в библиотеку
    def add_book(self, book):
        self.books.append(book)  # Добавляем книгу в список
        print(f"\nКнига '{book.title}' успешно добавлена в библиотеку.\n")  # Сообщаем об успешном добавлении

    # Метод для отображения всех книг
    def display_all_books(self):
        if self.books:  # Проверяем, есть ли книги в библиотеке
            print("\nВсе книги в библиотеке:")
            for book in self.books:  # Проходим по каждой книге
                book.display_info()  # Выводим информацию о книге
                print('-' * 40)  # Разделитель для удобства чтения
        else:
            print("\nВ библиотеке нет книг.\n")  # Если книг нет, выводим сообщение

    # Метод для загрузки начального набора книг
    def load_initial_books(self):
        initial_books = [
            Book("Убить пересмешника", "Харпер Ли", 1960, 281),
            Book("Великий Гэтсби", "Фрэнсис Скотт Фицджеральд", 1925, 218),
            DigitalBook("Моби Дик", "Герман Мелвилл", 1851, 635, "PDF"),
            DigitalBook("451 градус по Фаренгейту", "Рэй Брэдбери", 1953, 194, "EPUB"),
            Book("Над пропастью во ржи", "Джером Дэвид Сэлинджер", 1951, 277)
        ]  # Список предварительно добавленных книг
        for book in initial_books:
            self.add_book(book)  # Добавляем каждую книгу в библиотеку

    # Метод для отображения меню
    def show_menu(self):
        while True:  # Бесконечный цикл для работы с меню
            print("\n--- Меню библиотеки ---")
            print("1. Добавить физическую книгу")
            print("2. Добавить цифровую книгу")
            print("3. Взять книгу")
            print("4. Вернуть книгу")
            print("5. Скачать цифровую книгу")
            print("6. Показать информацию о книге")
            print("7. Показать список всех книг")
            print("8. Найти книги по автору")
            print("9. Добавить отзыв к книге")
            print("10. Выйти")
            print("-------------------------")

            choice = input("Выберите действие: ")  # Получаем выбор пользователя

            # Проверяем выбор и вызываем соответствующий метод
            if choice == '1':
                self.add_physical_book()
            elif choice == '2':
                self.add_digital_book()
            elif choice == '3':
                self.take_book()
            elif choice == '4':
                self.return_book()
            elif choice == '5':
                self.download_digital_book()
            elif choice == '6':
                self.show_book_info()
            elif choice == '7':
                self.display_all_books()
            elif choice == '8':
                self.find_books_by_author()
            elif choice == '9':
                self.add_review_to_book()
            elif choice == '10':
                print("\nВыход из программы.\n")  # Сообщаем о выходе и выходим из цикла
                break
            else:
                print("\nНеверный выбор, попробуйте снова.\n")  # Если введено неверное значение

    # Метод для добавления физической книги
    def add_physical_book(self):
        title = input("\nВведите название книги: ")  # Получаем название книги
        author = input("Введите автора: ")  # Получаем имя автора
        year = self.get_valid_number("Введите год издания: ")  # Получаем год издания, проверив, что это число
        pages = self.get_valid_number("Введите количество страниц: ")  # Получаем количество страниц
        book = Book(title, author, year, pages)  # Создаем объект книги
        self.add_book(book)  # Добавляем книгу в библиотеку

    # Метод для добавления цифровой книги
    def add_digital_book(self):
        title = input("\nВведите название книги: ")  # Получаем название книги
        author = input("Введите автора: ")  # Получаем имя автора
        year = self.get_valid_number("Введите год издания: ")  # Получаем год издания
        pages = self.get_valid_number("Введите количество страниц: ")  # Получаем количество страниц
        file_format = input("Введите формат файла (например, PDF, EPUB): ")  # Получаем формат файла
        book = DigitalBook(title, author, year, pages, file_format)  # Создаем объект цифровой книги
        self.add_book(book)  # Добавляем книгу в библиотеку

    # Метод для взятия книги
    def take_book(self):
        title = input("\nВведите название книги, которую хотите взять: ")  # Получаем название книги
        book = self.find_book(title)  # Ищем книгу по названию
        if book:
            book.take_book()  # Если книга найдена, берем её
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")  # Если книга не найдена, выводим сообщение

    # Метод для возврата книги
    def return_book(self):
        title = input("\nВведите название книги, которую хотите вернуть: ")  # Получаем название книги
        book = self.find_book(title)  # Ищем книгу по названию
        if book:
            book.return_book()  # Если книга найдена, возвращаем её
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")  # Если книга не найдена, выводим сообщение

    # Метод для скачивания цифровой книги
    def download_digital_book(self):
        title = input("\nВведите название цифровой книги, которую хотите скачать: ")  # Получаем название книги
        book = self.find_book(title)  # Ищем книгу по названию
        if isinstance(book, DigitalBook):  # Проверяем, является ли книга цифровой
            book.download_book()  # Если да, скачиваем её
        else:
            print(f"\nЦифровая книга '{title}' не найдена.\n")  # Если не цифровая или не найдена, выводим сообщение

    # Метод для показа информации о книге
    def show_book_info(self):
        title = input("\nВведите название книги, информацию о которой хотите получить: ")  # Получаем название книги
        book = self.find_book(title)  # Ищем книгу по названию
        if book:
            book.display_info()  # Если книга найдена, выводим информацию
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")  # Если книга не найдена, выводим сообщение

    # Метод для поиска книг по автору
    def find_books_by_author(self):
        author = input("\nВведите имя автора: ")  # Получаем имя автора
        books_by_author = [book for book in self.books if book.author.lower() == author.lower()]  # Ищем книги по автору
        if books_by_author:  # Если книги найдены
            print(f"\nКниги автора {author}:")
            for book in books_by_author:  # Проходим по всем найденным книгам
                book.display_info()  # Выводим информацию о каждой книге
                print('-' * 40)  # Разделитель для удобства
        else:
            print(f"\nВ библиотеке нет книг автора {author}.\n")  # Если книг не найдено, выводим сообщение

    # Метод для добавления отзыва к книге
    def add_review_to_book(self):
        title = input("\nВведите название книги, к которой хотите добавить отзыв: ")  # Получаем название книги
        book = self.find_book(title)  # Ищем книгу по названию
        if book:
            review = input("Введите ваш отзыв: ")  # Получаем отзыв пользователя
            book.add_review(review)  # Добавляем отзыв к книге
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")  # Если книга не найдена, выводим сообщение

    # Метод для поиска книги по названию
    def find_book(self, title):
        for book in self.books:  # Проходим по всем книгам
            if book.title.lower() == title.lower():  # Проверяем, совпадает ли название
                return book  # Возвращаем найденную книгу
        return None  # Если книга не найдена, возвращаем None

    # Метод для проверки, что вводится число (год издания, страницы)
    def get_valid_number(self, prompt):
        while True:  # Бесконечный цикл для проверки корректности ввода
            try:
                return int(input(prompt))  # Пробуем преобразовать ввод в число
            except ValueError:
                print("Пожалуйста, введите числовое значение.")  # Если ввод не число, просим повторить


# Запуск программы
library = Library()  # Создаем объект библиотеки
library.show_menu()  # Вызываем метод для отображения меню

