import csv
import constants
import requests
import logging
from time import gmtime

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

last_refresh_time = None
all_dbs = [abilitiesDb, movesDb, pokemonDb, itemsDb, conditionsDb, naturesDb]


def attachMoves():
    retries = 0
    success = False

    rows = []
    while retries < 10 and not success:
        data = requests.get(constants.MOVE_POOL)
        csv_file = StringIO(data.text)

        reader = csv.reader(csv_file)
        rows = list(reader)
        logging.info("Number of rows in move pool sheet is %d.", len(rows))

        if len(rows) > 800:
            success = True
        else:
            logging.error(f"Retrieving move spreadsheet has failed {retries} times.")

        retries += 1

    logging.info("First few rows are:")
    for num, row in enumerate(rows):
        if num < 7:
            continue
        elif num > 15:
            break

        logging.info(row)


    start = False

    for pokemon_row in rows:
        if pokemon_row[1] == "Pokemon":
            start = True
            continue
        if start is False:
            continue
        if pokemon_row[4].startswith("No Movepool Data for this species and forme."):
            continue

        name = pokemon_row[1]
        if "-Mega" in name:
            name = f'Mega {name.replace("-Mega","")}'
        level0_move_list = pokemon_row[3].splitlines()
        level1_move_list = pokemon_row[4].splitlines()
        level2_move_list = pokemon_row[5].splitlines()
        level3_move_list = pokemon_row[6].splitlines()
        level4_move_list = pokemon_row[7].splitlines()

        if len(level0_move_list) + len(level1_move_list) + len(level2_move_list) + len(level3_move_list) + len(level4_move_list) <= 3:
            continue

        pokemon = pokemonDb.getPokemon(name)
        if name == "Cramorant-Gulping":
            pokemon = pokemonDb.getPokemon('cramorant')
        # Cramorant-Gulping is fuzzy searching to gulpin
        if pokemon_row[10] != "â\x80\x94":
            unevolved_pokemon = pokemonDb.getPokemon(pokemon_row[10])
            if not unevolved_pokemon.name in pokemon.name:
                unevolved_pokemon.is_fully_evolved = False
                for move in unevolved_pokemon.getMoves():
                    if unevolved_pokemon in move.pokemon_list:
                        move.pokemon_list.remove(unevolved_pokemon)

        if pokemon.movesList is None:
            level0_move_list_final = [movesDb.getMove(moveName) for moveName in level0_move_list]
            level1_move_list_final = [movesDb.getMove(moveName) for moveName in level1_move_list]
            level2_move_list_final = [movesDb.getMove(moveName) for moveName in level2_move_list]
            level3_move_list_final = [movesDb.getMove(moveName) for moveName in level3_move_list]
            level4_move_list_final = [movesDb.getMove(moveName) for moveName in level4_move_list]

            pokemon.movesList = [
                level0_move_list_final,
                level1_move_list_final,
                level2_move_list_final,
                level3_move_list_final,
                level4_move_list_final
            ]
            for level, move_level_list in enumerate(pokemon.movesList):
                for move in move_level_list:
                    if move.level is None:
                        move.level = level

            if pokemon.is_fully_evolved:
                for move in pokemon.getMoves():
                    move.pokemon_list.append(pokemon)

def set_up_abilities():
    for pokemon_name in pokemonDb.dictionary:
        pokemon = pokemonDb.dictionary[pokemon_name]
        if pokemon.is_fully_evolved:
            all_abilities = []
            if pokemon.abilities:
                all_abilities.extend(pokemon.abilities.split(','))
            if pokemon.hidden_ability:
                all_abilities.append(pokemon.hidden_ability)
            for ability in all_abilities:
                if ability != '?':
                    abilitiesDb.getAbility(ability).pokemon_list.append(pokemon)



def initialize_dbs():
    logging.info("Db initialization begins.")
    try:
        global last_refresh_time
        last_refresh_time = gmtime()
        for db in all_dbs:
            db.refresh_db()

        attachMoves()
        set_up_abilities()

        logging.info("Db initialization successful.")
    except Exception:
        logging.exception("An error occurred during DBs refresh")

