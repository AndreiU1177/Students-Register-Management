from src.service.service import Service
from src.exceptions import InvalidInput, InvalidId, InvalidGrade, InvalidDiscipline, UndoRedoException
from jproperties import Properties


class Ui:
    def __init__(self):
        self.__service = Service(*self.read_properties())

    def read_properties(self):
        configs = Properties()
        with open('settings.properties', 'rb') as config_file:
            configs.load(config_file)
        repository_type = configs.get('repository').data
        students_file = configs.get('students').data
        disciplines_file = configs.get('disciplines').data
        grades_file = configs.get('grades').data
        return repository_type, students_file, disciplines_file, grades_file

    def start(self):
        while True:
            try:
                self.printMenu()
                option = input(">>> ")
                option = option.strip()
                self.validate_main(option)
                if option == '1':
                    self.print_manage_ui()
                if option == '2':
                    self.print_grade_ui()
                if option == '3':
                    self.print_search_ui()
                if option == '4':
                    self.print_statistics_ui()
                if option == '5':
                    break
                if option == '6':
                    print("Undoing...")
                    self.__service.undo_redirect()
                if option == '7':
                    print("Redoing...")
                    self.__service.redo_redirect()

                print()
            except (InvalidInput, InvalidId, InvalidGrade, UndoRedoException) as ve:
                print(ve)

    def printMenu(self):
        print("This program is a Students Register Management.\n")
        print("1. Manage students and disciplines")
        print("2. Grade a student")
        print("3. Search")
        print("4. Statistics")
        print("5. Exit")
        print("6. Undo")
        print("7. Redo")

    def print_manage_ui(self):
        print("What do you want to manage?")
        print("1. Students")
        print("2. Disciplines")
        option = input(">>> ")
        option = option.strip()
        self.validate_manage(option)
        self.print_specific_manage_ui(option)

    def print_specific_manage_ui(self, option1):
        print("Choose what you want to do:")
        print("1. Add")
        print("2. Remove")
        print("3. Update")
        print("4. List")
        option = input(">>> ")
        option = option.strip()
        self.validate_specific_manage(option)
        if option == '1':
            self.add_ui(option1)
            self.__service.redo_clear()
        if option == '2':
            self.remove_ui(option1)
            self.__service.redo_clear()
        if option == '3':
            self.update_ui(option1)
            self.__service.redo_clear()
        if option == '4':
            self.list(option1)


    def print_grade_ui(self):
        stud_id = input("Enter the student id >>> ")
        discipline_id = input("Enter the discipline id >>> ")
        grade = input("Enter the grade >>> ")
        self.__service.grade_student_service(stud_id, discipline_id, grade)
        self.__service.redo_clear()
        print("Grading...")

    def print_search_ui(self):
        print("What are you searching for?")
        print("1. Student")
        print("2. Discipline")
        option1 = input(">>> ")
        option1 = option1.strip()
        self.validate_manage(option1)
        print("Based on what key you want to search?")
        print("1. ID")
        print("2. Name")
        option2 = input(">>> ")
        option2 = option2.strip()
        self.validate_manage(option2)
        key = input("Enter your search >>> ")
        lst = self.__service.search_service(option1, option2, key)
        print("Searching...")
        if len(lst) == 0:
            print("Nothing found")
        else:
            for elem in lst:
                print(elem)

    def print_statistics_ui(self):
        print("What statistics do you want to be displayed?")
        print("1. All students failing at one or more disciplines")
        print("2. Students with the best school situation")
        print("3. All disciplines at which there is at least one grade")
        option = input(">>> ")
        self.validate_statistics(option)
        lst = self.__service.statistics_service(option)
        for elem in lst:
            print(elem)


    def add_ui(self, entity):
        id = input("Enter id >>> ")
        name = input("Enter name >>> ")
        self.__service.add_service(entity, id, name)
        print("Adding...")

    def remove_ui(self, entity):
        id = input("Enter the id of the element to be removed >>> ")
        self.__service.remove_service(entity, id)
        print("Removing...")

    def update_ui(self, entity):
        id = input("Enter id of the element to be updated >>> ")
        new_name = input("Enter the new name for the selected entity >>> ")
        self.__service.update_service(entity, id, new_name)
        print("Updating...")


    def list(self, entity):
        if entity == '1':
            self.print_students()
        else:
            self.print_disciplines()

    def print_students(self):
        students = self.__service.get_students_list()
        for student in students:
            print(student)
        print()

    def print_disciplines(self):
        disciplines = self.__service.get_disciplines_list()
        for discipline in disciplines:
            print(discipline)
        print()

    def validate_main(self, option):
        if not option.isdigit() or int(option) > 7 or int(option) < 1:
            raise InvalidInput("Command has to be an int between 1 and 5")

    def validate_manage(self, option):
        if not option.isdigit() or int(option) > 2 or int(option) < 1:
            raise InvalidInput("Command has to be either 1 or 2")

    def validate_specific_manage(self, option):
        if not option.isdigit() or int(option) > 4 or int(option) < 1:
            raise InvalidInput("Command has to be an int between 1 and 4")

    def validate_statistics(self, option):
        if not option.isdigit() or int(option) > 3 or int(option) < 1:
            raise InvalidInput("Command has to be an int between 1 and 3")
