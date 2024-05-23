import requests
import csv
import inflection
import discord
import json

from io import StringIO
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Move:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

class MoveDatabase:
    def __init__(self):
        self.populateDb()
    def populateDb(self):
        self.moves_dictionary = {}
        dat = requests.get("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=1023445923")
        csv_file = StringIO(dat.text)
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        for count, row in enumerate(rows):
            if(row["â\x97\x8f "]).startswith("-"):
                row["Name"] = row["â\x97\x8f "][1:]
                row.pop("â\x97\x8f ")
                row.pop("")
                row.pop("Combo Lv.")
                sanitized_row = {}
                for key in row.keys():
                    sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
                sanitized_row["Description"] = rows[count+1]["Type"]
                move = Move(**sanitized_row)
                self.moves_dictionary[row["Name"].lower()] = move