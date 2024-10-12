import random

class Book:
    def __init__(self, title, author, year, pages, available=None):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.available = available if available is not None else random.choice([True, False])
        self.reviews = []

    def display_info(self):
        availability = "доступна" if self.available else "недоступна"
        print(f"\nНазвание: {self.title}\nАвтор: {self.author}\nГод издания: {self.year}\nСтраниц: {self.pages}\nСтатус: {availability}\n")
        self.display_reviews()

    def take_book(self):
        if self.available:
            self.available = False
            print(f"\nВы взяли книгу: {self.title}\n")
        else:
            print(f"\nКнига '{self.title}' сейчас недоступна.\n")

    def return_book(self):
        if not self.available:
            self.available = True
            print(f"\nКнига '{self.title}' успешно возвращена в библиотеку.\n")
        else:
            print(f"\nКнига '{self.title}' уже была доступна.\n")

    def add_review(self, review):
        self.reviews.append(review)
        print(f"\nВаш отзыв добавлен для книги '{self.title}'.\n")

    def display_reviews(self):
        if self.reviews:
            print("Отзывы:")
            for review in self.reviews:
                print(f"- {review}")
        else:
            print("Отзывов пока нет. Будьте первым!")

    @staticmethod
    def display_random_review():
        reviews = [
            "Эта книга меня впечатлила!",
            "Отличное произведение, обязательно прочтите.",
            "Немного скучновато, но достойно внимания.",
            "Эта книга затянула меня с первой страницы!",
            "Интересная, но с сложным сюжетом. Советую."
        ]
        print(f"Отзыв: {random.choice(reviews)}\n")


class DigitalBook(Book):
    def __init__(self, title, author, year, pages, file_format, available=None):
        super().__init__(title, author, year, pages, available)
        self.file_format = file_format

    def display_info(self):
        super().display_info()
        print(f"Формат файла: {self.file_format}\n")

    def download_book(self):
        if self.available:
            print(f"\nВы скачали цифровую книгу: {self.title} в формате {self.file_format}.\n")
        else:
            print(f"\nЦифровая книга '{self.title}' недоступна для скачивания.\n")


class Library:
    def __init__(self):
        self.books = []
        self.load_initial_books()

    def add_book(self, book):
        self.books.append(book)
        print(f"\nКнига '{book.title}' успешно добавлена в библиотеку.\n")

    def display_all_books(self):
        if self.books:
            print("\nВсе книги в библиотеке:")
            for book in self.books:
                book.display_info()
                print('-' * 40)
        else:
            print("\nВ библиотеке нет книг.\n")

    def load_initial_books(self):
        initial_books = [
            Book("Убить пересмешника", "Харпер Ли", 1960, 281),
            Book("Великий Гэтсби", "Фрэнсис Скотт Фицджеральд", 1925, 218),
            DigitalBook("Моби Дик", "Герман Мелвилл", 1851, 635, "PDF"),
            DigitalBook("451 градус по Фаренгейту", "Рэй Брэдбери", 1953, 194, "EPUB"),
            Book("Над пропастью во ржи", "Джером Дэвид Сэлинджер", 1951, 277)
        ]
        for book in initial_books:
            self.add_book(book)

    def show_menu(self):
        while True:
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

            choice = input("Выберите действие: ")

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
                print("\nВыход из программы.\n")
                break
            else:
                print("\nНеверный выбор, попробуйте снова.\n")

    def add_physical_book(self):
        title = input("\nВведите название книги: ")
        author = input("Введите автора: ")
        year = self.get_valid_number("Введите год издания: ")
        pages = self.get_valid_number("Введите количество страниц: ")
        book = Book(title, author, year, pages)
        self.add_book(book)

    def add_digital_book(self):
        title = input("\nВведите название книги: ")
        author = input("Введите автора: ")
        year = self.get_valid_number("Введите год издания: ")
        pages = self.get_valid_number("Введите количество страниц: ")
        file_format = input("Введите формат файла (например, PDF, EPUB): ")
        book = DigitalBook(title, author, year, pages, file_format)
        self.add_book(book)

    def take_book(self):
        title = input("\nВведите название книги, которую хотите взять: ")
        book = self.find_book(title)
        if book:
            book.take_book()
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")

    def return_book(self):
        title = input("\nВведите название книги, которую хотите вернуть: ")
        book = self.find_book(title)
        if book:
            book.return_book()
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")

    def download_digital_book(self):
        title = input("\nВведите название цифровой книги, которую хотите скачать: ")
        book = self.find_book(title)
        if isinstance(book, DigitalBook):
            book.download_book()
        else:
            print(f"\nКнига '{title}' не является цифровой или её нет в библиотеке.\n")

    def show_book_info(self):
        title = input("\nВведите название книги: ")
        book = self.find_book(title)
        if book:
            book.display_info()
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")

    def find_books_by_author(self):
        author = input("\nВведите имя автора: ")
        books_by_author = [book for book in self.books if book.author.lower() == author.lower()]
        if books_by_author:
            print(f"\nКниги автора {author}:")
            for book in books_by_author:
                book.display_info()
                print('-' * 40)
        else:
            print(f"\nВ библиотеке нет книг автора {author}.\n")

    def add_review_to_book(self):
        title = input("\nВведите название книги, к которой хотите добавить отзыв: ")
        book = self.find_book(title)
        if book:
            review = input("Введите ваш отзыв: ")
            book.add_review(review)
        else:
            print(f"\nКнига '{title}' не найдена в библиотеке.\n")

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def get_valid_number(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Пожалуйста, введите числовое значение.")


# Запуск программы
library = Library()
library.show_menu()
