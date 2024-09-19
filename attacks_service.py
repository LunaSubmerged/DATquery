from type_calculator import typesDictionary
from type_calculator import getTypeChart
from functools import partial


def effectiveBap(move, pokemon):
    _return = 0
    if move.category != "Other" and move.bap != "--":
        if (move.bap == "??"):
            _return = -10
        elif (move.category == "Physical"):
            if (move.bap == "6 or 11"):
                _return = 6 + int(pokemon.atk)

            else:
                _return = int(move.bap) + int(pokemon.atk)
        else:
            _return = int(move.bap) + int(pokemon.sp_a)
    return int(_return)


def relativeEffectiveBap(move, pokemon1, pokemon2):
    _return = 0
    if move.category != "Other" and move.bap != "??" and move.bap != "--":
        if (move.bap == "??"):
            _return = -10
        elif (move.category == "Physical"):
            if (move.bap == "6 or 11"):
                _return = 6 + int(pokemon1.atk) - int(pokemon2.defence)
            else:
                _return = int(move.bap) + int(pokemon1.atk) - int(pokemon2.defence)
        else:
            _return = int(move.bap) + int(pokemon1.sp_a) - int(pokemon2.sp_d)
    return int(_return)


def calculateStrongestAttacks(pokemon, level):
    moves = []

    for n in range(level + 1):
        moves = moves + pokemon.movesList[n]

    highestBapMoves = {}

    for pokemonType in typesDictionary:
        highestBapMoves[pokemonType] = None

    for move in moves:
        comparitor = highestBapMoves[move.type.lower()]
        if (not move.category == "Other") and \
                (not move.bap == "??") and \
                ("deals fixed damage" not in move.description) and \
                (comparitor is None or effectiveBap(comparitor, pokemon) < effectiveBap(move, pokemon)):
            highestBapMoves[move.type.lower()] = move
    return highestBapMoves


def calculateSeAttacks(attacker, defender, level):
    localTypeChart = getTypeChart(defender)
    moves = []
    for n in range(level + 1):
        moves = moves + attacker.movesList[n]
    seAttackByType = {}
    sortedSeAttacksByType = {}
    for pokemonType in typesDictionary:
        seAttackByType[pokemonType] = []

    for move in moves:
        moveType = move.type.lower()
        if localTypeChart[typesDictionary[moveType]] >= 2 and move.category != "Other" and ("deals fixed damage" not in move.description):
            seAttackByType[moveType].append(move)

    for moveType in seAttackByType:
        if seAttackByType[moveType]:
            bapSort = partial(relativeEffectiveBap, pokemon1=attacker, pokemon2=defender)
            sortedList = seAttackByType[moveType]
            sortedList.sort(key=bapSort, reverse=True)
            sortedSeAttacksByType[moveType] = sortedList

    return sortedSeAttacksByType
