import inflection
import json
import utils
import constants

from databases.database import Database
from constants import BULLET


class Move:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)


class MoveDatabase(Database):
    def __init__(self):
        self.bullet_space = BULLET + " "
        super().__init__(constants.MOVES)

    def _process_rows(self, rows):
        for count, row in enumerate(rows):
            if (row[self.bullet_space]).startswith("-"):
                row["Name"] = row[self.bullet_space][1:]
                row.pop(self.bullet_space)
                row.pop("")
                row.pop("Combo Lv.")
                row["effect"] = row["Effect%"]
                row.pop("Effect%")
                row["contact"] = row["Contact?"]
                row["snatch"] = row["Snatch?"]
                row["reflect"] = row["Reflect?"]
                row.pop("Contact?")
                row.pop("Snatch?")
                row.pop("Reflect?")
                sanitized_row = {}
                for key in row.keys():
                    sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
                sanitized_row["description"] = rows[count + 1]["Type"]
                if "\n" in sanitized_row["description"]:
                    fluff, description = sanitized_row["description"].split("\n", 1)
                    sanitized_row["fluff"] = fluff
                    sanitized_row["description"] = description
                else:
                    sanitized_row["fluff"] = sanitized_row["description"]
                    sanitized_row["description"] = ""

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
