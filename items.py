import requests
import csv
import inflection
from io import StringIO
import discord

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Item:
    def __init__(self, **fields):
        self.__dict__.update(fields)
    def print_function(self, string):
        pass

class ItemDatabase:
    def __init__(self):
        self.populateDb()
    def populateDb(self):
        self.items_dictionary = {}

        dat = requests.get("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=2023973583")
        csv_file = StringIO(dat.text)
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Item"].startswith("-"):
                local_item = {}
                local_item["name"] = row["Item"][1:]
                local_item["description"] = row["Description"].replace("â", "-")
                item = Item(**local_item)
                self.items_dictionary[local_item["name"].lower()] = item
            

    def getItem(self, name):
        l_name = name.lower()
        fuzzy = process.extract(name, self.items_dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]
        if fuzzyName in self.items_dictionary:
            return (self.items_dictionary[fuzzyName])


    def ItemInfo(self, item):
        if item != None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = item.name,
                description = item.description
            )
            return embed