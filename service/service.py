from src.utils.exceptions import InvalidInput, InvalidId, InvalidGrade, InvalidDiscipline
from src.repository.memoryRepo import Repository
from src.repository.pickleRepo import PickleRepository
from src.repository.textfileRepo import TextRepository
from src.service.undo_service import Command, Operation, UndoService, CascadedOperation


class Service:
    def __init__(self, repo_type, students_file, disciplines_file, grades_file):
        if repo_type == 'inmemory':
            self._repo = Repository()
            self._repo.generate_entities()
        if repo_type == 'textfiles':
            self._repo = TextRepository(students_file, disciplines_file, grades_file)
            self._repo.generateTextfiles()
        if repo_type == 'binaryfiles':
            self._repo = PickleRepository(students_file, disciplines_file, grades_file)
            self._repo.generatePicklefiles()
        self.__undo_service = UndoService()

    def undo_redirect(self):
        self.__undo_service.undo()

    def redo_redirect(self):
        self.__undo_service.redo()

    def get_students_list(self):
        return self._repo.get_students_list()

    def get_disciplines_list(self):
        return self._repo.get_disciplines_list()

    def add_service(self, entity, id, name):
        """
        Adds student/discipline
        :param entity: '1' for student, '2' for discipline
        :param id: id of the new entity
        :param name: name of the new entity
        :return: adding
        """
        self.validate_id_notexists(id, entity)
        if entity == '1':
            self._repo.add_student(id, name)
            undo_action = Command(self._repo.remove_student, id)
            redo_action = Command(self._repo.add_student, id, name)
            operation = Operation(undo_action, redo_action)
            self.__undo_service.undo_append(operation)
        else:
            self.validate_discipline_notexists(name)
            self._repo.add_discipline(id, name)
            undo_action = Command(self._repo.remove_discipline, id)
            redo_action = Command(self._repo.add_discipline, id, name)
            operation = Operation(undo_action, redo_action)
            self.__undo_service.undo_append(operation)

    def remove_service(self, entity, id):
        """
        Removes student/discipline
        :param entity: '1' for student, '2' for discipline
        :param id: id of the entity to be deleted
        :return: removing
        """
        self.validate_id_exists(id, entity)
        if entity == '1':
            removed_student, removed_grades = self._repo.remove_student(id)
            undo_action = Command(self._repo.add_student, id, removed_student.get_student_name())
            redo_action = Command(self._repo.remove_student, id)
            operation = Operation(undo_action, redo_action)
            cascaded_ops = [operation]
            for grade in removed_grades:
                undo_action = Command(self._repo.grade_student, grade.get_student_id(), grade.get_discipline_id(), grade.get_grade_value())
                redo_action = Command(self._repo.ungrade_student, grade.get_student_id(), grade.get_discipline_id(), grade.get_grade_value())
                op = Operation(undo_action, redo_action)
                cascaded_ops.append(op)
            self.__undo_service.undo_append(CascadedOperation(cascaded_ops))
        else:
            removed_discipline, removed_grades = self._repo.remove_discipline(id)
            undo_action = Command(self._repo.add_discipline, id, removed_discipline.get_discipline_name())
            redo_action = Command(self._repo.remove_discipline, id)
            operation = Operation(undo_action, redo_action)
            cascaded_ops = [operation]
            for grade in removed_grades:
                undo_action = Command(self._repo.grade_student, grade.get_student_id(), grade.get_discipline_id(),
                                      grade.get_grade_value())
                redo_action = Command(self._repo.ungrade_student, grade.get_student_id(), grade.get_discipline_id(),
                                      grade.get_grade_value())
                op = Operation(undo_action, redo_action)
                cascaded_ops.append(op)
            self.__undo_service.undo_append(CascadedOperation(cascaded_ops))

    def update_service(self, entity, id, new_name):
        """
        Updates the name of a student/discipline
        :param entity: '1' for student, '2' for discipline
        :param id: id of the entity to be updated
        :param new_name: the new name that will be assigned
        :return: updating
        """
        self.validate_id_exists(id, entity)
        if entity == '1':
            old_name = self._repo.update_student(id, new_name)
            undo_action = Command(self._repo.update_student, id, old_name)
            redo_action = Command(self._repo.update_student, id, new_name)
            operation = Operation(undo_action, redo_action)
            self.__undo_service.undo_append(operation)
        else:
            old_name = self._repo.update_discipline(id, new_name)
            undo_action = Command(self._repo.update_discipline, id, old_name)
            redo_action = Command(self._repo.update_discipline, id, new_name)
            operation = Operation(undo_action, redo_action)
            self.__undo_service.undo_append(operation)

    def grade_student_service(self, student_id, discipline_id, grade_value):
        self.validate_id_exists(student_id, '1')
        self.validate_id_exists(discipline_id, '2')
        self.validate_grade(grade_value)
        added_grade = self._repo.grade_student(student_id, discipline_id, grade_value)
        undo_action = Command(self._repo.ungrade_student, added_grade.get_student_id(), added_grade.get_discipline_id(), added_grade.get_grade_value())
        redo_action = Command(self._repo.grade_student, student_id, discipline_id, grade_value)
        operation = Operation(undo_action, redo_action)
        self.__undo_service.undo_append(operation)

    def ungrade_student_service(self, student_id, discipline_id, grade_value):
        return self._repo.ungrade_student(student_id, discipline_id, grade_value)

    def search_service(self, entity, criteria, key):
        if entity == '1':
            if criteria == '1':
                return self._repo.search_student_by_id(key)
            else:
                return self._repo.search_student_by_name(key)
        else:
            if criteria == '1':
                return self._repo.search_discipline_by_id(key)
            else:
                return self._repo.search_discipline_by_name(key)

    def statistics_service(self, option):
        if option == '1':
            return self.failing_students()
        if option == '2':
            return self.best_situation_students()
        if option == '3':
            return self.disciplines_with_grades()

    def failing_students(self):
        students = self._repo.get_students_list()
        disciplines = self._repo.get_disciplines_list()
        grades = self._repo.get_grades_list()
        failing_students = []
        for student in students:
            failing = False
            for discipline in disciplines:
                average = 0
                count = 0
                for grade in grades:
                    if grade.get_student_id() == student.get_student_id() and grade.get_discipline_id() == discipline.get_discipline_id():
                        average += grade.get_grade_value()
                        count += 1
                if count != 0:
                    average /= count
                    if average < 5:
                        failing = True
                        break
            if failing:
                failing_students.append(student)
        return failing_students

    def best_situation_students(self):
        students = self._repo.get_students_list()
        disciplines = self._repo.get_disciplines_list()
        grades = self._repo.get_grades_list()
        average_grades = {}
        for student in students:
            average_grade = []
            for discipline in disciplines:
                average = 0
                count = 0
                for grade in grades:
                    if grade.get_student_id() == student.get_student_id() and grade.get_discipline_id() == discipline.get_discipline_id():
                        average += grade.get_grade_value()
                        count += 1
                if count != 0:
                    average /= count
                    average_grade.append(average)
            if len(average_grade) != 0:
                sum = 0
                for value in average_grade:
                    sum += value
                result = sum / len(average_grade)
                result = round(result, 2)
                average_grades[student.get_student_id()] = [result, student.get_student_name()]
        average_grades = sorted(average_grades.items(), key=lambda item: item[1][0], reverse=True)
        returned_list = []
        for key in average_grades:
            returned_list.append(str(key[0]) + ' ' + str(key[1][1]) + ' ' + str(key[1][0]))
        return returned_list

    def disciplines_with_grades(self):
        students = self._repo.get_students_list()
        disciplines = self._repo.get_disciplines_list()
        grades = self._repo.get_grades_list()
        disciplines_with_averages = []
        for discipline in disciplines:
            grades_for_discipline = 0
            students_with_discipline_grade = 0
            for student in students:
                grade_for_discipline_for_student = 0
                count = 0
                for grade in grades:
                    if grade.get_student_id() == student.get_student_id() and grade.get_discipline_id() == discipline.get_discipline_id():
                        grade_for_discipline_for_student += grade.get_grade_value()
                        count += 1
                if count != 0:
                    average_for_student = round(grade_for_discipline_for_student / count, 2)
                    students_with_discipline_grade += 1
                    grades_for_discipline += average_for_student
            if students_with_discipline_grade != 0:
                average_grade = round(grades_for_discipline / students_with_discipline_grade, 2)
                disciplines_with_averages.append([discipline.get_discipline_id(), discipline.get_discipline_name(), average_grade])
        disciplines_with_averages = sorted(disciplines_with_averages, key=lambda item: item[2], reverse=True)
        returned_list = []
        for elem in disciplines_with_averages:
            returned_list.append(str(elem[0]) + ' ' + str(elem[1]) + ' ' + str(elem[2]))
        return returned_list


    def validate_id_notexists(self, id, entity):
        if not id.isdigit():
            raise InvalidInput("ID consists only of digits")
        if entity == '1':
            students = self.get_students_list()
            for student in students:
                if student.get_student_id() == id:
                    raise InvalidInput("A student with this ID already exists")
        if entity == '2':
            disciplines = self.get_disciplines_list()
            for discipline in disciplines:
                if discipline.get_discipline_id() == id:
                    raise InvalidInput("A discipline with this ID already exists")

    def validate_id_exists(self, id, entity):
        if not id.isdigit():
            raise InvalidInput("ID consists only of digits")
        found = False
        if entity == '1':
            students = self.get_students_list()
            for student in students:
                if student.get_student_id() == id:
                    found = True
        if entity == '2':
            disciplines = self.get_disciplines_list()
            for discipline in disciplines:
                if discipline.get_discipline_id() == id:
                    found = True
        if not found:
            raise InvalidId("ID not found")

    def validate_grade(self, grade):
        if grade.find('.') != grade.rfind('.'):
            raise InvalidGrade("Invalid grade")

        if not grade.replace(".", "").isnumeric():
            raise InvalidGrade("Grade should be a number")

        if not 0 < float(grade) <= 10:
            raise InvalidGrade("Grade should be a number in range (0, 10]")

    def validate_discipline_notexists(self, name):
        disciplines = self.get_disciplines_list()
        for discipline in disciplines:
            if discipline.get_discipline_name() == name:
                raise InvalidDiscipline("A discipline with this name already exists")

    def redo_clear(self):
        self.__undo_service.clear_redo_stack()
