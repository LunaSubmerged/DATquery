import requests
import csv
import inflection
from io import StringIO
import discord
import constants

from database import Database
from fuzzywuzzy import fuzz
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
        if row["Ability"] != "":
            local_ability = {}
            local_ability["name"] = row["Ability"][1:]
            local_ability["description"] = row["Description"]
            ability = Ability(**local_ability)
            self.dictionary[local_ability["name"].lower()] = ability
            

    def getAbility(self, name):
        l_name = name.lower()
        fuzzy = process.extract(name, self.dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]
        if fuzzyName in self.dictionary:
            return (self.dictionary[fuzzyName])


    def abilityInfo(self, ability):
        if ability != None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = ability.name,
                description = ability.description
            )
            return embed