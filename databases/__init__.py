import csv
import constants
import requests

from io import StringIO
from databases.moves_db import MoveDatabase
from databases.abilities_db import AbilityDatabase
from databases.pokemon_db import PokemonDatabase
from databases.conditions_db import ConditionDatabase
from databases.natures_db import NatureDatabase
from databases.items_db import ItemDatabase


movesDb = MoveDatabase()
pokemonDb = PokemonDatabase()
abilitiesDb = AbilityDatabase()
conditionsDb = ConditionDatabase()
itemsDb = ItemDatabase()
naturesDb = NatureDatabase()

all_dbs = [abilitiesDb, movesDb, pokemonDb, itemsDb, conditionsDb, naturesDb]


def attachMoves():
    data = requests.get(constants.MOVE_POOL)
    csv_file = StringIO(data.text)
    reader = csv.reader(csv_file)
    rows = list(reader)

    start = False

    for row in rows:
        if row[1] == "Pokemon":
            start = True
            continue

        if start:
            pokemonRow = row
            if pokemonRow[4].startswith("No Movepool Data for this species and forme."):
                continue

            name = pokemonRow[1]

            level0MoveList = pokemonRow[3].splitlines()
            level1MoveList = pokemonRow[4].splitlines()
            level2MoveList = pokemonRow[5].splitlines()
            level3MoveList = pokemonRow[6].splitlines()
            level4MoveList = pokemonRow[7].splitlines()

            if len(level0MoveList) + len(level1MoveList) + len(level2MoveList) + len(level3MoveList) + len(level4MoveList) <= 3:
                continue

            pokemon = pokemonDb.getPokemon(name)

            if pokemon.movesList is None:
                level0MoveListFinal = [movesDb.getMove(moveName) for moveName in level0MoveList]
                level1MoveListFinal = [movesDb.getMove(moveName) for moveName in level1MoveList]
                level2MoveListFinal = [movesDb.getMove(moveName) for moveName in level2MoveList]
                level3MoveListFinal = [movesDb.getMove(moveName) for moveName in level3MoveList]
                level4MoveListFinal = [movesDb.getMove(moveName) for moveName in level4MoveList]

                pokemon.movesList = [
                    level0MoveListFinal,
                    level1MoveListFinal,
                    level2MoveListFinal,
                    level3MoveListFinal,
                    level4MoveListFinal
                ]

def intitialize_dbs():
    for db in all_dbs:
        db.refresh_db()

    attachMoves()
