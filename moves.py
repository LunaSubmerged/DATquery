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
                sanitized_row["description"] = rows[count+1]["Type"].replace("â", "-")
                move = Move(**sanitized_row)
                self.moves_dictionary[row["Name"].lower()] = move

    
    def getMove(self, name):
        l_name = name.lower()
        fuzzy = process.extract(name, self.moves_dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]

        if fuzzyName in self.moves_dictionary:
            return (self.moves_dictionary[fuzzyName])

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
