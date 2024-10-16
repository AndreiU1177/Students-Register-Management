import random
import re

from src.domain.grade import Grade
from src.domain.discipline import Discipline
from src.domain.student import Student


class Repository:
    def __init__(self):
        self._students = []
        self._disciplines = []
        self._grades = []

        for grade in self._grades:
            print(grade)

    def get_students_list(self):
        return self._students

    def get_disciplines_list(self):
        return self._disciplines

    def get_grades_list(self):
        return self._grades

    def add_student(self, new_id, new_name):
        """
        Adds student to database
        :param new_id: new student id
        :param new_name: new student name
        :return: adding new student
        """
        new_student = Student(new_id, new_name)
        self._students.append(new_student)

    def add_discipline(self, new_id, new_name):
        """
        Adds discipline to database
        :param new_id: new discipline id
        :param new_name: new discipline name
        :return: adding discipline
        """
        new_discipline = Discipline(new_id, new_name)
        self._disciplines.append(new_discipline)

    def remove_student(self, id):
        """
        Removes a student from database based on id
        :param id: id of student to be removed
        :return: removing student
        Also remove grades assigned to the student
        """
        i = 0
        while i < len(self._students):
            student = self._students[i]
            if student.get_student_id() == id:
                deleted_student = self._students.pop(i)
                i -= 1
            i += 1

        removed_grades = []
        i = 0
        while i < len(self._grades):
            grade = self._grades[i]
            if grade.get_student_id() == id:
                removed = self.ungrade_student(id, grade.get_discipline_id(), grade.get_grade_value())
                removed_grades.append(removed)
                i -= 1
            i += 1
        return deleted_student, removed_grades

    def remove_discipline(self, id):
        """
        Removes a discipline from database based on id
        :param id: id of discipline to be removed
        :return: removing discipline
        Also remove grades that are from this discipline
        """
        i = 0
        while i < len(self._disciplines):
            discipline = self._disciplines[i]
            if discipline.get_discipline_id() == id:
                deleted_discipline = self._disciplines.pop(i)
                i -= 1
            i += 1

        deleted_grades = []
        i = 0
        while i < len(self._grades):
            grade = self._grades[i]
            if grade.get_discipline_id() == id:
                deleted = self.ungrade_student(grade.get_student_id(), id, grade.get_grade_value())
                deleted_grades.append(deleted)
                i -= 1
            i += 1
        return deleted_discipline, deleted_grades

    def update_student(self, id, new_name):
        """
        Update student name based on id
        :param id: id of student to be updated
        :param new_name: new name of the student
        :return: updating name
        """
        for student in self._students:
            if student.get_student_id() == id:
                old_name = student.get_student_name()
                student.set_student_name(new_name)
        return old_name

    def update_discipline(self, id, new_name):
        """
        Updates discipline name based on id
        :param id: id of discipline to be updated
        :param new_name: new name of the discipline
        :return: updating name
        """
        for discipline in self._disciplines:
            if discipline.get_discipline_id() == id:
                old_name = discipline.get_discipline_name()
                discipline.set_discipline_name(new_name)
        return old_name

    def grade_student(self, student_id, discipline_id, grade_value):
        grade = Grade(discipline_id, student_id, float(grade_value))
        self._grades.append(grade)
        return grade

    def ungrade_student(self, student_id, discipline_id, grade_value):
        i = 0
        while i < len(self._grades):
            grade = self._grades[i]
            if grade.get_grade_value() == grade_value and grade.get_student_id() == student_id and grade.get_discipline_id() == discipline_id:
                deleted_grade = self._grades.pop(i)
                i -= 1
            i += 1
        return deleted_grade

    def search_student_by_id(self, key):
        lst = []
        for student in self._students:
            if re.search(key, student.get_student_id(), re.IGNORECASE):
                lst.append(student)
        return lst

    def search_student_by_name(self, key):
        lst = []
        for student in self._students:
            if re.search(key, student.get_student_name(), re.IGNORECASE):
                lst.append(student)
        return lst

    def search_discipline_by_id(self, key):
        lst = []
        for discipline in self._disciplines:
            if re.search(key, discipline.get_discipline_id(), re.IGNORECASE):
                lst.append(discipline)
        return lst

    def search_discipline_by_name(self, key):
        lst = []
        for discipline in self._disciplines:
            if re.search(key, discipline.get_discipline_name(), re.IGNORECASE):
                lst.append(discipline)
        return lst

    def generate_entities(self):
        students = [
            ['123', 'Alice Smith'],
            ['234', 'Bob Johnson'],
            ['345', 'Charlie Williams'],
            ['456', 'David Jones'],
            ['567', 'Eva Brown'],
            ['678', 'Frank Davis'],
            ['789', 'Grace Miller'],
            ['890', 'Hannah Wilson'],
            ['901', 'Ian Moore'],
            ['012', 'Julia Taylor'],
            ['112', 'Liam Martinez'],
            ['223', 'Olivia Anderson'],
            ['334', 'Noah Thompson'],
            ['445', 'Sophia Garcia'],
            ['556', 'Mia Hernandez'],
            ['667', 'Benjamin Lopez'],
            ['778', 'Emma Gonzalez'],
            ['889', 'William Perez'],
            ['990', 'Ava Rodriguez'],
            ['000', 'James Ramirez']
        ]
        for elem in students:
            student = Student(elem[0], elem[1])
            self._students.append(student)

        disciplines = [
            ['101', 'Computer Science'],
            ['202', 'Mathematics'],
            ['303', 'Physics'],
            ['404', 'Biology'],
            ['505', 'Chemistry'],
            ['606', 'History'],
            ['707', 'English'],
            ['808', 'Psychology'],
            ['909', 'Sociology'],
            ['010', 'Economics'],
            ['111', 'Anthropology'],
            ['212', 'Geography'],
            ['313', 'Political Science'],
            ['414', 'Philosophy'],
            ['515', 'Art'],
            ['616', 'Music'],
            ['717', 'Drama'],
            ['818', 'Business'],
            ['919', 'Engineering'],
            ['020', 'Health Sciences']
        ]
        for elem in disciplines:
            discipline = Discipline(elem[0], elem[1])
            self._disciplines.append(discipline)

        # discipline_id`, `student_id`, `grade_value
        for i in range(0, 20):
            grade = [random.choice(disciplines)[0], random.choice(students)[0], round(random.uniform(1, 10), 2)]
            entity_grade = Grade(grade[0], grade[1], grade[2])
            self._grades.append(entity_grade)
