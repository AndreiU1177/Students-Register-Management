from src.domain.student import Student
from src.domain.discipline import Discipline

class Grade(Student, Discipline):
    def __init__(self, discipline_id, student_id, grade_value):
        self._discipline_id = discipline_id
        self._student_id = student_id
        self._grade_value = grade_value

    def get_grade_value(self):
        return self._grade_value

    def __str__(self):
        return "Discipline id: {}, Student id: {}, Grade: {}".format(self._discipline_id, self._student_id, self._grade_value)
        