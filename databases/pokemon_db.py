import inflection
import utils
import constants

from databases.database import Database


class Pokemon:
    def __init__(self, **fields):
        self.__dict__.update(fields)
        self.movesList = None
        self.is_fully_evolved = True


    def get_moves(self):
        moves_list = []
        if self.movesList is not None:
            for move_level_list in self.movesList:
                for move in move_level_list:
                    moves_list.append(move)

        return moves_list

    def get_moves_level(self, level):
        moves_list = []
        if self.movesList is not None:
            for n in range(level + 1):
                for move in self.movesList[n]:
                    moves_list.append(move)

        return moves_list

    def print_function(self, string):
        pass


class PokemonDatabase(Database):
    def __init__(self):
        super().__init__(constants.POKEMON)

    def _build_dictionary(self, row):
        name = ""
        if "Name" in row:
            name = row["Name"]
        if "" in row:
            row.pop("")
        if "Reference Functions" in row:
            row.pop("Reference Functions")
        if "Bot Notation Column" in row:
            row.pop("Bot Notation Column")
        if name == "POKEMON":
            return
        sanitized_row = {}
        for key in row.keys():
            sanitized_row[inflection.underscore(key.replace(" ", ""))] = row[key]
        if "Def" in row:
            sanitized_row["defence"] = row["Def"]
            sanitized_row.pop("def")
        if "signature_moveor_moves" in sanitized_row:
            sanitized_row["signature_move"] = sanitized_row["signature_moveor_moves"]
            sanitized_row.pop("signature_moveor_moves")

        aliases = {
            'basculin-blue-striped': 'basculin-bluestriped',
            'basculin-white-striped': 'basculin-whitestriped',
            'charizard-mega-x': 'charizard-megax',
            'charizard-mega-y': 'charizard-megay',
            'chien-pao': 'chienpao',
            'chi-yu': 'chiyu',
            'darmanitan-galar-zen': 'darmanitan-galarzen',
            "farfetch'd": 'farfetchd',
            'gourgeist-small': 'gourgeist',
            'gourgeist-average': 'gourgeist',
            'gourgeist-large': 'gourgeist',
            'gourgeist-super': 'gourgeist',
            'greninja-bond': 'greninja',
            'hakamo-o': 'hakamoo',
            'ho-oh': 'hooh',
            'indeedee-m': 'indeedee',
            'kommo-o': 'kommoo',
            'meowstic-m': 'meowstic',
            'mewtwo-mega-x': 'mewtwo-megax',
            'mewtwo-mega-y': 'mewtwo-megay',
            'necrozma-dawn-wings': 'necrozma-dawnwings',
            'necrozma-dusk-mane': 'necrozma-duskmane',
            'oricorio-baile': 'oricorio',
            "oricorio-pa'u": 'oricorio-pau',
            'porygon-z': 'porygonz',
            'pumpkaboo-small': 'pumpkaboo',
            'pumpkaboo-average': 'pumpkaboo',
            'pumpkaboo-large': 'pumpkaboo',
            'pumpkaboo-super': 'pumpkaboo',
            'rockruff-dusk': 'rockruff',
            'rotom-spin': 'rotom-fan',
            'rotom-freeze': 'rotom-frost',
            'rotom-cut': 'rotom-mow',
            "sirfetch'd": 'sirfetchd',
            'tauros-paldea-combat': 'tauros-paldeacombat',
            'tauros-paldea-blaze': 'tauros-paldeablaze',
            'tauros-paldea-aqua': 'tauros-paldeaaqua',
            'ting-lu': 'tinglu',
            'toxtricity-low-key': 'toxtricity-lowkey',
            'urshifu-rapid-strike': 'urshifu-rapidstrike',
            'wo-chien': 'wochien',
            'zygarde-10%': 'zygarde-10'
        }
        if "showdown_alias" in sanitized_row:
            if name.lower() in aliases:
                sanitized_row["showdown_alias"] = aliases[name.lower()]
            elif sanitized_row["showdown_alias"] == "":
                sanitized_row["showdown_alias"] = name.lower().replace(" ", "")
            else:
                sanitized_row["showdown_alias"] = sanitized_row["showdown_alias"].lower()

        pokemon = Pokemon(**sanitized_row)
        self.dictionary[name.lower()] = pokemon

    def getPokemon(self, name):
        return utils.fuzzySearch(name, self.dictionary)
