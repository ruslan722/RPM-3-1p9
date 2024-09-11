from models import Book, biblioteka
# Инициализация базы данных
biblioteka()
# Класс для управления библиотекой
class Library:
    def __init__(self):
        # Загрузка всех книг из базы данных
        self.update_books()
    def update_books(self):
        # Обновление списка книг из базы данных
        self.books = Book.select()
    # Метод для добавления книги в библиотеку
    def add_book(self, book):
        book.save()  # Сохранение книги в базу данных
        self.update_books()  # Обновление списка книг
    # Метод для показа списка книг
    def show_books(self):
        if not self.books:
            print("Библиотека пуста.")
        else:
            for i, book in enumerate(self.books, 1):
                print(f"{i}. {book.title}")
    # Метод для взятия книги по индексу
    def take_book(self, book_index):
        if 0 <= book_index < len(self.books):
            book = self.books[book_index]
            if book.dostup:
                book.dostup = False
                book.save()
                #сохранили
                print(f"Вы взяли книгу: {book.title}")
            else:
                print(f"Книга '{book.title}' уже на руках.")
        else:
            print("Некорректный индекс книги.")
        self.update_books()  # Обновление списка книг
    # Метод для возврата книги по индексу
    def return_book(self, book_index):
        if 0 <= book_index < len(self.books):
            book = self.books[book_index]
            if not book.dostup:
                book.dostup = True
                book.save()
                print(f"Вы вернули книгу: {book.title}")
            else:
                print(f"Книга '{book.title}' уже находится в библиотеке.")
        else:
            print("Некорректный индекс книги.")
        self.update_books()  # Обновление списка книг
def create_book():
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = int(input("Введите год издания книги: "))
    pages = int(input("Введите количество страниц книги: "))
    return Book(title=title, author=author, year=year, pages=pages)
def menu():
    library = Library()
    while True:
        print("\nМеню:")
        print("1. Взять книгу")
        print("2. Вернуть книгу")
        print("3. Показать информацию о книгах")
        print("4. Добавить новую книгу")
        print("5. Выйти")
        choice = input("Выберите опцию: ")
        if choice == "1":
            library.show_books()
            if library.books:
                index = int(input("Введите номер книги, которую хотите взять: ")) - 1
                library.take_book(index)
        elif choice == "2":
            library.show_books()
            if library.books:
                index = int(input("Введите номер книги, которую хотите вернуть: ")) - 1
                library.return_book(index)
        elif choice == "3":
            library.show_books()
            for book in library.books:
                status = "Доступна" if book.dostup else "На руках у пользователя"
                print(f"'{book.title}' by {book.author} ({book.year}, {book.pages} стр.), статус: {status}")
        elif choice == "4":
            new_book = create_book()
            library.add_book(new_book)
            print(f"Книга '{new_book.title}' добавлена в библиотеку.")
        elif choice == "5":
            print("Выход из программы.")
            break
if __name__ == "__main__":
    menu()