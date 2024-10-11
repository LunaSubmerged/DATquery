from type_calculator import typesDictionary
from type_calculator import get_type_chart_pokemon
from functools import partial


def effective_bap(move, pokemon):
    _return = 0
    if move.category != "Other" and move.bap != "--":
        if move.bap == "??":
            _return = -10
        elif move.category == "Physical":
            if move.bap == "6 or 11":
                _return = 6 + int(pokemon.atk)

            else:
                _return = int(move.bap) + int(pokemon.atk)
        else:
            _return = int(move.bap) + int(pokemon.sp_a)
    return int(_return)


def relative_effective_bap(move, pokemon1, pokemon2):
    _return = 0
    if move.category != "Other" and move.bap != "??" and move.bap != "--":
        if move.bap == "??":
            _return = -10
        elif move.category == "Physical":
            if move.bap == "6 or 11":
                _return = 6 + int(pokemon1.atk) - int(pokemon2.defence)
            else:
                _return = int(move.bap) + int(pokemon1.atk) - int(pokemon2.defence)
        else:
            _return = int(move.bap) + int(pokemon1.sp_a) - int(pokemon2.sp_d)
    return int(_return)


def calculate_strongest_attacks(pokemon, level):
    moves = []

    for n in range(level + 1):
        moves = moves + pokemon.movesList[n]

    highest_bap_moves = {}

    for pokemonType in typesDictionary:
        highest_bap_moves[pokemonType] = None

    for move in moves:
        comparator = highest_bap_moves[move.type.lower()]
        if (not move.category == "Other") and \
                (not move.bap == "??") and \
                ("deals fixed damage" not in move.description) and \
                (comparator is None or effective_bap(comparator, pokemon) < effective_bap(move, pokemon)):
            highest_bap_moves[move.type.lower()] = move
    return highest_bap_moves


def calculate_se_attacks(attacker, defender, level):
    local_type_chart = get_type_chart_pokemon(defender)
    moves = []
    for n in range(level + 1):
        moves = moves + attacker.movesList[n]
    se_attack_by_type = {}
    sorted_se_attacks_by_type = {}
    for pokemonType in typesDictionary:
        se_attack_by_type[pokemonType] = []

    for move in moves:
        move_type = move.type.lower()
        if local_type_chart[typesDictionary[move_type]] >= 2 and move.category != "Other" and ("deals fixed damage" not in move.description):
            se_attack_by_type[move_type].append(move)

    for move_type in se_attack_by_type:
        if se_attack_by_type[move_type]:
            bap_sort = partial(relative_effective_bap, pokemon1=attacker, pokemon2=defender)
            sorted_list = se_attack_by_type[move_type]
            sorted_list.sort(key=bap_sort, reverse=True)
            sorted_se_attacks_by_type[move_type] = sorted_list

    return sorted_se_attacks_by_type


def count_moves_by_type(pokemon):
    moves = []
    for n in range(5):
        moves = moves + pokemon.movesList[n]
    _count_phys = 0
    _count_spec = 0
    _count_other = 0
    for move in moves:
        if move.category == "Physical":
            _count_phys += 1
        elif move.category == "Special":
            _count_spec += 1
        elif move.category == "Other":
            _count_other += 1
    return [_count_phys, _count_spec, _count_other]
