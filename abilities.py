import requests
import csv
import inflection
from io import StringIO
import discord

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Ability:
    def __init__(self, **fields):
        self.__dict__.update(fields)
    def print_function(self, string):
        pass

class AbilityDatabase:
    def __init__(self):
        self.populateDb()
    def populateDb(self):
        self.abilities_dictionary = {}

        dat = requests.get("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=1445814381")
        csv_file = StringIO(dat.text)
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Ability"] != "":
                local_ability = {}
                local_ability["name"] = row["Ability"][1:]
                local_ability["description"] = row["Description"]
                ability = Ability(**local_ability)
                self.abilities_dictionary[local_ability["name"].lower()] = ability
            

    def getAbility(self, name):
        l_name = name.lower()
        fuzzy = process.extract(name, self.abilities_dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]
        if fuzzyName in self.abilities_dictionary:
            return (self.abilities_dictionary[fuzzyName])


    def abilityInfo(self, ability):
        if ability != None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = ability.name,
                description = ability.description
            )
            return embed