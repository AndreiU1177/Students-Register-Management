

class Student:
    def __init__(self, student_id, name):
        self._student_id = student_id
        self._student_name = name

    def get_student_id(self):
        return self._student_id

    def get_student_name(self):
        return self._student_name

    def set_student_name(self, new_name):
        self._student_name = new_name

    def __str__(self):
        return "Student_id: {}, Name: {}".format(self._student_id, self._student_name)

