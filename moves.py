import requests
import csv
import inflection
from io import StringIO
import discord

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class MoveDatabase:
    def __init__(self):
        dat = requests.get("https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/export?format=csv&gid=1023445923")
        csv_file = StringIO(dat.text)
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)

movesDatabase = MoveDatabase()