import inflection
import json
import utils
import constants

from databases.database import Database
from constants import BULLET


class Move:
    def __init__(self, **fields):
        self.__dict__.update(fields)
        self.pokemon_list = []
        self.level = None

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)


class MoveDatabase(Database):
    def __init__(self):
        self.bullet_space = BULLET + " "
        super().__init__(constants.MOVES)

    def _process_rows(self, rows):
        for count, row in enumerate(rows):
            if self.bullet_space in row and row[self.bullet_space].startswith("-"):
                row["Name"] = row[self.bullet_space][1:]
                row.pop(self.bullet_space)
                if "" in row:
                    row.pop("")
                if "Effect%" in row:
                    row["effect"] = row["Effect%"]
                    row.pop("Effect%")
                if "Contact?" in row:
                    row["contact"] = row["Contact?"]
                    row.pop("Contact?")
                if "Snatch?" in row:
                    row["snatch"] = row["Snatch?"]
                    row.pop("Snatch?")
                if "Reflect?" in row:
                    row["reflect"] = row["Reflect?"]
                    row.pop("Reflect?")
                if "Combo Lv." in row:
                    row["combo_lvl"] = row["Combo Lv."]
                    row.pop("Combo Lv.")
                sanitized_row = {}
                for key in row.keys():
                    sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
                if "Type" in row:
                    sanitized_row["description"] = rows[count + 1]["Type"]
                    if "\n" in sanitized_row["description"]:
                        fluff, description = sanitized_row["description"].split("\n", 1)
                        sanitized_row["fluff"] = fluff
                        sanitized_row["description"] = description
                    else:
                        sanitized_row["fluff"] = sanitized_row["description"]
                        sanitized_row["description"] = ""

                if "Tags" in row:
                    sanitized_row["contest_description"] = rows[count + 1]["Tags"]
                    if "\n" in sanitized_row["contest_description"]:
                        constest_fluff, contest_description = sanitized_row["contest_description"].split("\n", 1)
                        sanitized_row["contest_fluff"] = constest_fluff
                        sanitized_row["contest_description"] = contest_description
                    else:
                        sanitized_row["contest_fluff"] = sanitized_row["contest_description"]
                        sanitized_row["contest_description"] = ""

                move = Move(**sanitized_row)
                self.dictionary[row["Name"].lower()] = move

    def getMove(self, name):
        return utils.fuzzySearch(name, self.dictionary)

    def emptyDiscordSpace(self, int):
        return "\u1CBC" * int
