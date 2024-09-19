import constants

from databases.database import Database
from fuzzywuzzy import process


class Ability:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def print_function(self, string):
        pass


class AbilityDatabase(Database):
    def __init__(self):
        super().__init__(constants.ABILITIES)

    def _build_dictionary(self, row):
        if row["Ability"].startswith("-"):
            local_ability = {}
            local_ability["name"] = row["Ability"][1:]
            fluff, description = row["Description"].split("\n", 1)
            local_ability["fluff"] = fluff
            local_ability["description"] = description
            ability = Ability(**local_ability)
            self.dictionary[local_ability["name"].lower()] = ability

    def getAbility(self, name):
        fuzzy = process.extract(name, self.dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]
        if fuzzyName in self.dictionary:
            return (self.dictionary[fuzzyName])
