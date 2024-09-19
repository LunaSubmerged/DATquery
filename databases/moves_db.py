import inflection
import discord
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

    def moveInfo(self, move):
        if move is not None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = move.name,
                description = f"*{move.fluff}*"
            )
            if move.description != "":
                embed.add_field(name="Description", value=move.description, inline=False)
            embed.add_field(name="Category", value = move.category)
            embed.add_field(name="Type", value = move.type)
            embed.add_field(name="Accuracy", value = move.acc)
            embed.add_field(name="BAP", value= move.bap)
            embed.add_field(name="Energy Cost", value=move.en_cost)
            embed.add_field(name="Target", value= move.target)
            embed.add_field(name="Effect Chance", value= move.effect)
            embed.add_field(name="Priority", value= move.priority)
            embed.add_field(name="Tags", value= move.tags)
            embed.add_field(name="Additional Info", value = f'Contact: {move.contact} \n Reflect: {move.reflect}')
            embed.add_field(name="\u1CBC", value = f'Snatch: {move.snatch}')

        return embed

    def contestInfo(self, move):
        if move is not None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = move.name,
                description = f"*{move.contest_fluff}*"
            )
            if move.description != "":
                embed.add_field(name="Description", value=move.contest_description, inline=False)
            embed.add_field(name="Tags", value= move.tags)
            embed.add_field(name="Genre", value= move.genre)
            embed.add_field(name="Appeal", value= move.appeal)
            embed.add_field(name="Jam", value= move.jam)
        return embed