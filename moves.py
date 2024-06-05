import requests
import csv
import inflection
import discord
import json

from database import Database
from constants import BULLET
from io import StringIO
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Move:
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

class MoveDatabase(Database):
    def __init__(self):
        self.bullet_space = BULLET + " "
        super().__init__("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=1023445923")
        

    def _process_rows(self, rows):       
        for count, row in enumerate(rows):
            if(row[self.bullet_space]).startswith("-"):
                row["Name"] = row[self.bullet_space][1:]
                row.pop(self.bullet_space)
                row.pop("")
                row.pop("Combo Lv.")
                row["effect"] = row["Effect%"]
                row.pop("Effect%")
                row["contact"] = row["Contact?"]
                row["snatch"]= row["Snatch?"]
                row["reflect"] = row["Reflect?"]
                row.pop("Contact?")
                row.pop("Snatch?")
                row.pop("Reflect?")
                sanitized_row = {}
                for key in row.keys():
                    sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
                sanitized_row["description"] = rows[count+1]["Type"]
                move = Move(**sanitized_row)
                self.dictionary[row["Name"].lower()] = move

    
    def getMove(self, name):
        l_name = name.lower()
        fuzzy = process.extract(name, self.dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]

        if fuzzyName in self.dictionary:
            return (self.dictionary[fuzzyName])

    def emptyDiscordSpace(self, int):
        return "\u1CBC" * int
    
    def moveInfo(self, move):
        if move != None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = move.name,
                description = move.description
            )
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
