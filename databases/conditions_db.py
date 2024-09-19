import constants

from databases.database import Database
from fuzzywuzzy import process


class Condition:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def print_function(self, string):
        pass


class ConditionDatabase(Database):
    def __init__(self):
        super().__init__(constants.CONDITIONS)

    def _build_dictionary(self, row):
        if row["Condition"].startswith("-"):
            local_condition = {}
            local_condition["name"] = row["Condition"][1:]
            fluff, description = row["Description"].split("\n", 1)
            local_condition["fluff"] = fluff
            local_condition["description"] = description
            local_condition["default_duration"] = row["Default Duration"]
            condition = Condition(**local_condition)
            self.dictionary[local_condition["name"].lower()] = condition

    def getCondition(self, name):
        fuzzy = process.extract(name, self.dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]
        if fuzzyName in self.dictionary:
            return (self.dictionary[fuzzyName])
