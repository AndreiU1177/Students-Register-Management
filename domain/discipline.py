

class Discipline:
    def __init__(self, discipline_id, name):
        self._discipline_id = discipline_id
        self._discipline_name = name

    def get_discipline_id(self):
        return self._discipline_id

    def get_discipline_name(self):
        return self._discipline_name

    def set_discipline_name(self, new_name):
        self._discipline_name = new_name

    def __str__(self):
        return "Discipline_id: {}, Name: {}".format(self._discipline_id, self._discipline_name)

