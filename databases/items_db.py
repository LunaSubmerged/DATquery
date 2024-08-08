import discord
import utils
import constants

from databases.database import Database

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
            fluff, description = row["Description"].split("\n", 1)
            local_item["fluff"] = fluff
            local_item["description"] = description
            item = Item(**local_item)
            self.dictionary[local_item["name"].lower()] = item
            

    def getItem(self, name):
        return utils.fuzzySearch(name, self.dictionary)


    def ItemInfo(self, item):
        if item != None:
            embed = discord.Embed(
                color = discord.Color.dark_teal(),
                title = item.name,
                description = f"*{item.fluff}*"
            )
            embed.add_field(name = "Description", value = item.description, inline=False)
            return embed