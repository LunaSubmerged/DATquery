import requests
import csv
import inflection
import discord

from io import StringIO
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from database import Database

class Pokemon:
    def __init__(self, **fields):
        self.__dict__.update(fields)
    def print_function(self, string):
        pass


class PokemonDatabase(Database):
    def __init__(self):        
        super().__init__("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=2042923402")
       
       
    def _build_dictionary(self, row):
        name = row["Name"]
        row.pop("")
        row.pop("Reference Functions")
        row.pop("Bot Notation Column")
        row["SignatureMoveOrMoves"] = row.pop("Signature Move or Moves")
        sanitized_row = {}
        for key in row.keys():
            sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
        sanitized_row["defence"] = row["Def"]
        sanitized_row.pop("def")

        pokemon = Pokemon(**sanitized_row)
        if sanitized_row["id"] == "Mega":
            self.dictionary["mega_" + name.lower()] = pokemon
        else:
            self.dictionary[name.lower()] = pokemon
        

    def getPokemon(self, name):
        l_name = name.lower()
        fuzzy = process.extract(name, self.dictionary.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]

        if fuzzyName in self.dictionary:
            return (self.dictionary[fuzzyName])
            self.dictionary[fuzzyName].print_function("TODO")

            
    def pokemonInfo(self, pokemon):
        if pokemon != None:
          embed = discord.Embed(
              color = discord.Color.dark_teal(),
              title = pokemon.name,
              description = pokemon.typing
          )
          sprite = pokemon.name.lower().replace(" ", "")
          if pokemon.sprite_alias != "":
              sprite = pokemon.sprite_alias.lower()
          embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + sprite + ".png")
          embed.add_field(name="Abilities", value = pokemon.abilities)
          embed.add_field(name="Hidden Ability", value = pokemon.hidden_ability)
          line1 = "HP: " + pokemon.hp
          line2 = "ATK: " + pokemon.atk + " | DEF: " + pokemon.defence + " | SpA: " + pokemon.sp_a + " | SpD: " + pokemon.sp_d
          line3 = "Speed: " + pokemon.spe
          line4 = "Size Class: " + pokemon.size
          line5 = "Weight Class: " + pokemon.weight
          embed.add_field(name="Stats", value = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5,  inline= False)

          return (embed)