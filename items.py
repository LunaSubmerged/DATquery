import requests
import csv
import inflection
from io import StringIO
import discord
import utils
import constants

from database import Database
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class Item:
    def __init__(self, **fields):
        self.__dict__.update(fields)
    def print_function(self, string):
        pass

class ItemDatabase(Database):
    def __init__(self):
        super().__init__(constants.ITEMS)
   
    def _build_dictionary(self, row):
        if row["Item"].startswith("-"):
            local_item = {}
            local_item["name"] = row["Item"][1:]
            local_item["description"] = row["Description"]
            item = Item(**local_item)
            self.dictionary[local_item["name"].lower()] = item
            

    def getItem(self, name):
        return utils.fuzzySearch(name, self.dictionary)


    def ItemInfo(self, item):
        if item != None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = item.name,
                description = item.description
            )
            return embed