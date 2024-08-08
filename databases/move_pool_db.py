import requests
import csv
import inflection
import discord
import constants

from io import StringIO
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from databases.database import Database


data = requests.get(constants.MOVE_POOL)

csv_file = StringIO(data.text)
reader = csv.reader(csv_file)
rows = list(reader)
for row in rows:
    row.pop(2)
    row.pop(0)
for count, row in enumerate(list(rows)):
    print(count)
    print(row[0])
    if row[0] == "":
        rows.pop(0)
    else:
        break

keys = []
for header in rows[0]:
    keys.append(header)
print(keys)
rows.pop(0)
print(rows[0])
for pokemon in rows:
    name = pokemon[0]
    level0MoveList = pokemon[1].splitlines()
    level1MoveList = pokemon[2].splitlines()
    level2MoveList = pokemon[3].splitlines()
    level3MoveList = pokemon[4].splitlines()
    level4MoveList = pokemon[5].splitlines()
    print(level0MoveList)