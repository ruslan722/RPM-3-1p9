import random
# Базовый класс Person, который содержит общие данные о человеке (имя и возраст)
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
# Класс Student расширяет класс Person
# Реализуем конструктор класса Student с приватными атрибутами для предметов и оценок
class Student(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.__grades = {}  # Приватный атрибут для хранения оценок по предметам
        self.__subjects = self._generate_random_subjects()  # Приватный атрибут для хранения списка предметов студента
    # Приватный метод для генерации случайного набора предметов для студента
    def _generate_random_subjects(self):
        base_subjects = ["Математика", "Психология", "Геометрия", "История", "Английский"]  # Базовые предметы
        additional_subjects = self._generate_random_subject_names(3)  # Дополнительно генерируем 3 случайных предмета
        all_subjects = base_subjects + additional_subjects  # Объединяем базовые и случайные предметы
        return random.sample(all_subjects, 8)  # Выбираем 8 случайных предметов
    # Приватный метод для генерации случайных имён предметов на основе префиксов и суффиксов
    def _generate_random_subject_names(self, count):
        prefixes = ["Физ", "Хим", "Инфо", "Био", "Эко", "Астро", "Техно", "Лингво", "Филосо"]
        suffixes = ["логия", "метрия", "графия", "номика", "логия", "физика", "техника", "дизайн", "математика"]
        subjects = []
        for _ in range(count):
            subject_name = random.choice(prefixes) + random.choice(suffixes)  # Генерируем случайное имя предмета
            subjects.append(subject_name)
        return subjects
    # Свойство для доступа к списку предметов студента
    @property
    def subjects(self):
        return self.__subjects
    # Метод для добавления оценки студенту по конкретному предмету
    # Используем инкапсуляцию: проверяем, что предмет присутствует в списке предметов
    def add_grade(self, subject, grade):
        if subject in self.__subjects:  # Если предмет есть у студента
            if subject not in self.__grades:
                self._grades[subject] = []  # Если предмета нет в списке оценок, создаем его
            self.__grades[subject].append(grade)  # Добавляем оценку по предмету
        else:
            print(f"{subject} не является предметом у студента {self.name}. Доступные предметы: {', '.join(self.__subjects)}")
    # Метод для вычисления средней оценки студента
    # Используем инкапсуляцию для доступа к приватным оценкам
    def get_average_grade(self):
        total_grades = sum([sum(grades) for grades in self.__grades.values()])  # Суммируем все оценки
        total_subjects = sum([len(grades) for grades in self.__grades.values()])  # Считаем количество предметов с оценками
        return total_grades / total_subjects if total_subjects > 0 else 0  # Возвращаем среднюю оценку
    # Метод для вывода информации о студенте, включая предметы с оценками
    def __str__(self):
        avg_grade = self.get_average_grade()  # Вычисляем среднюю оценку
        graded_subjects = [f"{subject}: {self.__grades[subject]}" for subject in self.__grades]  # Формируем список предметов с оценками
        if graded_subjects:
            graded_subjects_str = ', '.join(graded_subjects)  # Форматируем строку с предметами и оценками
        else:
            graded_subjects_str = "Оценок пока нет."  # Если нет оценок, выводим соответствующее сообщение
        return f"Имя: {self.name}, Возраст: {self.age}, Средняя оценка: {avg_grade:.2f}, Предметы с оценками: {graded_subjects_str}"
# Класс для управления студентами
class StudentManagementSystem:
    def __init__(self):
        self.students = []  # Список студентов в системе
    # Метод для добавления студента в систему
    def add_student(self, name, age):
        student = Student(name, age)
        self.students.append(student)  # Добавляем нового студента в список
        print(f"Студент {name}, {age} лет добавлен в систему.")
    # Метод для добавления оценки студенту по предмету
    def add_grade_to_student(self, student_name, subject, grade):
        student = self._find_student_by_name(student_name)  # Находим студента по имени
        if student:
            student.add_grade(subject, grade)  # Добавляем оценку
    # Метод для показа информации обо всех студентах в системе
    def show_students(self):
        if self.students:
            for student in self.students:
                print(student)  # Выводим информацию о каждом студенте
        else:
            print("Нет студентов в системе.")
    # Метод для сортировки студентов по средней оценке в порядке убывания
    def sort_students_by_average_grade(self):
        sorted_students = sorted(self.students, key=lambda s: s.get_average_grade(), reverse=True)  # Сортируем по средней оценке
        for student in sorted_students:
            print(student)  # Выводим информацию о каждом студенте
    # Метод для показа студента с наивысшей средней оценкой
    def show_best_student(self):
        if self.students:
            best_student = max(self.students, key=lambda s: s.get_average_grade())  # Находим студента с максимальной средней оценкой
            print(f"Лучший студент: {best_student}")
        else:
            print("Нет студентов в системе.")
    # Приватный метод для поиска студента по имени
    def _find_student_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student  # Возвращаем студента, если имя совпадает
        print(f"Студент с именем {name} не найден.")
        return None
# Основное меню программы
def main():
    system = StudentManagementSystem()
    while True:
        print("\nМеню:")
        print("1. Добавить студента")
        print("2. Добавить оценку студенту")
        print("3. Показать информацию о студентах")
        print("4. Сортировать студентов по средней оценке")
        print("5. Показать лучшего студента")
        print("6. Выйти")
        choice = input("Выберите действие: ")
        if choice == '1':
            name = input("Введите имя студента: ")
            age = int(input("Введите возраст студента: "))
            system.add_student(name, age)  # Добавляем нового студента
        elif choice == '2':
            name = input("Введите имя студента: ")
            student = system._find_student_by_name(name)
            if student:
                print(f"Предметы студента {name}: {', '.join(student.subjects)}")  # Показываем доступные предметы
                subject = input("Введите название предмета: ")
                grade = float(input("Введите оценку: "))
                system.add_grade_to_student(name, subject, grade)  # Добавляем оценку
        elif choice == '3':
            system.show_students()  # Показать информацию о студентах
        elif choice == '4':
            system.sort_students_by_average_grade()  # Сортировать студентов по средней оценке
        elif choice == '5':
            system.show_best_student()  # Показать лучшего студента
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
if __name__ == "__main__":
    main()