import inflection
import utils
import constants

from databases.database import Database


class Pokemon:
    def __init__(self, **fields):
        self.__dict__.update(fields)
        self.movesList = None
        self.is_fully_evolved = True


    def getMoves(self):
        moves_list = []
        if self.movesList is not None:
            for move_level_list in self.movesList:
                for move in move_level_list:
                    moves_list.append(move)

        return moves_list

    def print_function(self, string):
        pass


class PokemonDatabase(Database):
    def __init__(self):
        super().__init__(constants.POKEMON)

    def _build_dictionary(self, row):
        name = row["Name"]
        row.pop("")
        row.pop("Reference Functions")
        row.pop("Bot Notation Column")
        sanitized_row = {}
        for key in row.keys():
            sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
        sanitized_row["defence"] = row["Def"]
        sanitized_row.pop("def")
        sanitized_row["signature_move"] = sanitized_row["signature_moveor_moves"]
        sanitized_row.pop("signature_moveor_moves")
        if sanitized_row["showdown_alias"] == "":
            sanitized_row["showdown_alias"] = name.lower().replace(" ", "")
        else:
            sanitized_row["showdown_alias"] = sanitized_row["showdown_alias"].lower()

        pokemon = Pokemon(**sanitized_row)
        if sanitized_row["id"] == "Mega":
            pokemon.name = "Mega " + pokemon.name
            self.dictionary["mega_" + name.lower()] = pokemon
        elif sanitized_row["id"] == "Primal":
            pokemon.name = "Primal " + pokemon.name
            self.dictionary["primal_" + name.lower()] = pokemon
        else:
            self.dictionary[name.lower()] = pokemon

    def getPokemon(self, name):
        return utils.fuzzySearch(name, self.dictionary)
