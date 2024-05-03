import discord
from discord.ext import commands
import requests
import csv
import json
import inflection

from io import StringIO

class Pokemon:
    def __init__(self, **fields):
        self.__dict__.update(fields)
    def print_function(self, string):
        pass


class PokemonDatabase:
    def __init__(self):
        self.pokemon_dictionary = {}

        dat = requests.get("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=2042923402")
        csv_file = StringIO(dat.text)
        reader = csv.DictReader(csv_file)

        for row in reader:
            name = row["Name"]
            row.pop("")
            row.pop("Reference Functions")
            row.pop("Bot Notation Column")
            row["SignatureMoveOrMoves"] = row.pop("Signature Move or Moves")
            sanitized_row = {}
            for key in row.keys():
                sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]

            pokemon = Pokemon(**sanitized_row)
            if sanitized_row["id"] == "Mega":
                self.pokemon_dictionary["mega_" + name.lower()] = pokemon
            else:
                self.pokemon_dictionary[name.lower()] = pokemon

    def pokemonInfo(self, name):
        l_name = name.lower()
        if l_name.startswith("mega"):
            pass
        if l_name in self.pokemon_dictionary:
            return (json.dumps(self.pokemon_dictionary[l_name].__dict__, indent = 4))
            self.pokemon_dictionary[l_name].print_function("TODO")
        else:
            return f'"{name}" is not a recognised pokemon.'

intents = discord.Intents.all()

# Initialize bot with intents
bot = commands.Bot(command_prefix='%', intents=intents)
db = PokemonDatabase()
@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.listen("on_message")
async def on_message(message):
    if message.content == "ping":
        await message.channel.send("pong")
@bot.command()
async def stats(ctx, arg):
    await ctx.send(db.pokemonInfo(arg))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
# Run bot
bot.run('gitSafe')