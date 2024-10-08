import requests
import csv
from io import StringIO
import constants

from databases.database import Database
from fuzzywuzzy import process


class Nature:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def print_function(self, string):
        pass


class NatureDatabase(Database):
    def __init__(self):
        super().__init__(constants.NATURES)

    def _build_dictionary(self, row):
        local_nature = {}
        if row[0] != "" and row[0] != "Pokemon Natures":
            local_nature["name"] = row[0]
            local_nature["description"] = row[1]
            nature = Nature(**local_nature)
            self.dictionary[local_nature["name"].lower()] = nature

    def refresh_db(self):
        dat = requests.get(self.url)
        dat.encoding = "utf-8"
        csv_file = StringIO(dat.text)
        reader = csv.reader(csv_file)
        rows = list(reader)
        self._process_rows(rows)

    def getNature(self, name):
        fuzzy = process.extract(name, self.dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]
        if fuzzyName in self.dictionary:
            return (self.dictionary[fuzzyName])

