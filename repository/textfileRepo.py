import os

from src.domain.student import Student
from src.repository.memoryRepo import Repository

class TextRepository(Repository):
    def __init__(self, students_file, disciplines_file, grades_file):
        super().__init__()
        self.students_file = students_file
        self.disciplines_file = disciplines_file
        self.grades_file = grades_file
        self.read_students()
        self.read_disciplines()
        self.read_grades()

    def read_students(self):
        file = open(self.students_file, 'r')
        elements = file.readlines()
        for string in elements:
            string = string[:-1]
            if string == '\n':
                break
            splitted = string.split(' ', 1)
            id, name = splitted
            super().add_student(id, name)
        file.close()

    def read_disciplines(self):
        file = open(self.disciplines_file, 'r')
        elements = file.readlines()
        for string in elements:
            string = string[:-1]
            if string == '\n':
                break
            splitted = string.split(' ', 1)
            id, name = splitted
            super().add_discipline(id, name)
        file.close()

    def read_grades(self):
        file = open(self.grades_file, 'r')
        elements = file.readlines()
        for string in elements:
            string = string[:-1]
            if string == '\n':
                break
            splitted = string.split(' ')
            discipline_id, student_id, grade_value = splitted
            super().grade_student(student_id, discipline_id, grade_value)
        file.close()

    def add_student(self, new_id, new_name):
        super().add_student(new_id, new_name)
        file = open(self.students_file, 'a')
        file.writelines([str(new_id), ' ', str(new_name), '\n'])
        file.close()

    def add_discipline(self, new_id, new_name):
        super().add_discipline(new_id, new_name)
        file = open(self.disciplines_file, 'a')
        file.writelines([str(new_id), ' ', str(new_name), '\n'])
        file.close()

    def remove_student(self, id):
        deleted_student, deleted_grades = super().remove_student(id)
        file = open(self.students_file, 'w')
        for student in self.get_students_list():
            file.writelines([str(student.get_student_id()), ' ', str(student.get_student_name()), '\n'])
        file.close()
        file = open(self.grades_file, 'w')
        for existing_grade in self._grades:
            file.writelines([str(existing_grade.get_discipline_id()), ' ', str(existing_grade.get_student_id()), ' ', str(existing_grade.get_grade_value()), '\n'])
        file.close()
        return deleted_student, deleted_grades

    def remove_discipline(self, id):
        deleted_discipline, deleted_grades = super().remove_discipline(id)
        file = open(self.disciplines_file, 'w')
        for discipline in self.get_disciplines_list():
            file.write(str(discipline.get_discipline_id()) + ' ' + str(discipline.get_discipline_name()) + '\n')
        file.close()
        file = open(self.grades_file, 'w')
        for existing_grade in self._grades:
            file.write(str(existing_grade.get_discipline_id()) + ' ' + str(
                existing_grade.get_student_id()) + ' ' + str(existing_grade.get_grade_value()) + '\n')
        file.close()
        return deleted_discipline, deleted_grades

    def update_student(self, id, new_name):
        old_name = super().update_student(id, new_name)
        file = open(self.students_file, 'w')
        for student in self.get_students_list():
            file.write(str(student.get_student_id()) + ' ' + str(student.get_student_name()) + '\n')
        file.close()
        return old_name

    def update_discipline(self, id, new_name):
        old_name = super().update_discipline(id, new_name)
        file = open(self.disciplines_file, 'w')
        for discipline in self.get_disciplines_list():
            file.write(str(discipline.get_discipline_id()) + ' ' + str(discipline.get_discipline_name()) + '\n')
        file.close()
        return old_name

    def grade_student(self, student_id, discipline_id, grade_value):
        grade = super().grade_student(student_id, discipline_id, grade_value)
        file = open(self.grades_file, 'a')
        file.writelines([str(discipline_id) + ' ' + str(student_id) + ' ' + str(grade_value), '\n'])
        file.close()
        return grade

    def ungrade_student(self, student_id, discipline_id, grade_value):
        deleted_grade = super().ungrade_student(student_id, discipline_id, grade_value)
        file = open(self.grades_file, 'w')
        for grade in self.get_grades_list():
            file.write(str(grade.get_discipline_id()) + ' ' + str(grade.get_student_id()) + ' ' + str(grade.get_grade_value()) + '\n')
        return deleted_grade

    def generateTextfiles(self):
        if os.path.getsize(self.students_file) == 0:
            super().generate_entities()
        if os.path.getsize(self.students_file) == 0:
            file = open(self.students_file, 'w')
            for student in self.get_students_list():
                new_id, new_name = student.get_student_id(), student.get_student_name()
                file.writelines([str(new_id), ' ', str(new_name), '\n'])
            file.close()

        if os.path.getsize(self.disciplines_file) == 0:
            file = open(self.disciplines_file, 'w')
            for discipline in self.get_disciplines_list():
                new_id, new_name = discipline.get_discipline_id(), discipline.get_discipline_name()
                file.writelines([str(new_id), ' ', str(new_name), '\n'])
            file.close()

        if os.path.getsize(self.grades_file) == 0:
            file = open(self.grades_file, 'w')
            for grade in self.get_grades_list():
                discipline_id, student_id, grade_value = grade.get_discipline_id(), grade.get_student_id(), grade.get_grade_value()
                file.writelines([str(discipline_id), ' ', str(student_id), ' ', str(grade_value), '\n'])
            file.close()
