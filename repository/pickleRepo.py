import os
import pickle

from src.domain.student import Student
from src.repository.memoryRepo import Repository

class PickleRepository(Repository):
    def __init__(self, students_file, disciplines_file, grades_file):
        super().__init__()
        self.students_file = students_file
        self.disciplines_file = disciplines_file
        self.grades_file = grades_file
        self.read_students()
        self.read_disciplines()
        self.read_grades()
        for grade in self._grades:
            print(grade)

    def read_students(self):
        data = self.read_pickle(self.students_file)
        self._students = data

    def read_disciplines(self):
        data = self.read_pickle(self.disciplines_file)
        self._disciplines = data

    def read_grades(self):
        data = self.read_pickle(self.grades_file)
        self._grades = data

    def add_student(self, new_id, new_name):
        super().add_student(new_id, new_name)
        with open(self.students_file, 'wb') as file:
            pickle.dump(self.get_students_list(), file)

    def add_discipline(self, new_id, new_name):
        super().add_discipline(new_id, new_name)
        with open(self.disciplines_file, 'wb') as file:
            pickle.dump(self.get_disciplines_list(), file)

    def remove_student(self, id):
        deleted_student, deleted_grades = super().remove_student(id)
        with open(self.students_file, 'wb') as file:
            pickle.dump(self.get_students_list(), file)
        file = open(self.grades_file, 'w')
        with open(self.grades_file, 'wb') as file:
            pickle.dump(self.get_grades_list(), file)
        return deleted_student, deleted_grades

    def remove_discipline(self, id):
        deleted_discipline, deleted_grades = super().remove_discipline(id)
        with open(self.disciplines_file, 'wb') as file:
            pickle.dump(self.get_disciplines_list(), file)
        with open(self.grades_file, 'wb') as file:
            pickle.dump(self.get_grades_list(), file)
        return deleted_discipline, deleted_grades

    def update_student(self, id, new_name):
        old_name = super().update_student(id, new_name)
        with open(self.students_file, 'wb') as file:
            pickle.dump(self.get_students_list(), file)
        return old_name

    def update_discipline(self, id, new_name):
        old_name = super().update_discipline(id, new_name)
        with open(self.disciplines_file, 'wb') as file:
            pickle.dump(self.get_disciplines_list(), file)
        return old_name

    def grade_student(self, student_id, discipline_id, grade_value):
        grade = super().grade_student(student_id, discipline_id, grade_value)
        with open(self.grades_file, 'wb') as file:
            pickle.dump(grade, file)
        return grade

    def ungrade_student(self, student_id, discipline_id, grade_value):
        deleted_grade = super().ungrade_student(student_id, discipline_id, grade_value)
        with open(self.grades_file, 'wb') as file:
            pickle.dump(self.get_grades_list(), file)
        return deleted_grade

    def generatePicklefiles(self):
        if os.path.getsize(self.students_file) == 0:
            super().generate_entities()
        if os.path.getsize(self.students_file) == 0:
            with open(self.students_file, 'wb') as file:
                pickle.dump(self.get_students_list(), file)

        if os.path.getsize(self.disciplines_file) == 0:
            with open(self.disciplines_file, 'wb') as file:
                pickle.dump(self.get_disciplines_list(), file)

        if os.path.getsize(self.grades_file) == 0:
            with open(self.grades_file, 'wb') as file:
                pickle.dump(self.get_grades_list(), file)

    def read_pickle(self, file_name):
        data = []
        if os.path.getsize(file_name) != 0:
            with open(file_name, 'rb') as file:
                data = pickle.load(file)
        return data
