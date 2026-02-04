import utils
import constants

from databases.database import Database


class Discipline:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def print_function(self, string):
        pass


class DisciplineDatabase(Database):
    def __init__(self):
        super().__init__(constants.DISCIPLINES)

    def _build_dictionary(self, row):
        if row["Discipline"].startswith("-"):
            local_discipline = {}
            local_discipline["name"] = row["Discipline"][1:]
            local_discipline["level"] = row["Level"]
            local_discipline["flavor"] = row["Flavor Text"]
            local_discipline["effect"] = row["Effect Text"]
            local_discipline["tag"] = row["Tags"]
            discipline = Discipline(**local_discipline)
            self.dictionary[local_discipline["name"].lower()] = discipline

    def get_discipline(self, name):
        return utils.fuzzySearch(name, self.dictionary)
