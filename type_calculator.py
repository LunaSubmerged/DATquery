import discord

typesDictionary = {
    "bug": 0,
    "dark": 1,
    "dragon": 2,
    "electric": 3,
    "fairy": 4,
    "fighting": 5,
    "fire": 6,
    "flying": 7,
    "ghost": 8,
    "grass": 9,
    "ground": 10,
    "ice": 11,
    "normal": 12,
    "poison": 13,
    "psychic": 14,
    "rock": 15,
    "steel": 16,
    "water": 17
}

typeChart = [
    [1, 2, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 2, 1, 1, 1, 0.5, 2, 1, 0.5, 1],
    [1, 0.5, 1, 1, 0.5, 0.5, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1],
    [1, 1, 0.5, 0.5, 1, 1, 1, 2, 1, 0.5, 0, 1, 1, 1, 1, 1, 1, 2],
    [1, 2, 2, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 0.5, 1],
    [0.5, 2, 1, 1, 0.5, 1, 1, 0.5, 0, 1, 1, 2, 2, 0.5, 0.5, 2, 2, 1],
    [2, 1, 0.5, 1, 1, 1, 0.5, 1, 1, 2, 1, 2, 1, 1, 1, 0.5, 2, 0.5],
    [2, 1, 1, 0.5, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 0.5, 1],
    [1, 0.5, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2, 1, 1, 1],
    [0.5, 1, 0.5, 1, 1, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 2],
    [0.5, 1, 1, 2, 1, 1, 2, 0, 1, 0.5, 1, 1, 1, 2, 1, 2, 2, 1],
    [1, 1, 2, 1, 1, 1, 0.5, 2, 1, 2, 2, 0.5, 1, 1, 1, 1, 0.5, 0.5],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2, 0.5, 1, 1, 0.5, 1, 0.5, 0, 1],
    [1, 0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1],
    [2, 1, 1, 1, 1, 0.5, 2, 2, 1, 1, 0.5, 2, 1, 1, 1, 1, 0.5, 1],
    [1, 1, 1, 0.5, 2, 1, 0.5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 0.5, 0.5],
    [1, 1, 0.5, 1, 1, 1, 2, 1, 1, 0.5, 2, 1, 1, 1, 1, 2, 1, 0.5]
]


def get_type_defense_chart(type_id: int):
    type_defence_chart = []
    for offensive_type in typeChart:
        type_defence_chart.append(offensive_type[type_id])

    return type_defence_chart

def get_types_defense_chart(types_list):
    types_name_list = [pokemon_type.lower() for pokemon_type in types_list]
    types_defence_charts = []
    for pokemon_type in types_name_list:
        type_id = typesDictionary[pokemon_type]
        types_defence_charts.append(get_type_defense_chart(type_id))

    defence_chart_final = types_defence_charts.pop(0)
    for defence_chart in types_defence_charts:
        defence_chart_final = list(map(lambda x, y: x * y, defence_chart_final, defence_chart))

    return defence_chart_final

def get_type_offence_chart(type_id: int):
    return list(typeChart[type_id])

def get_type_chart_pokemon(pokemon):
    return get_types_defense_chart(pokemon.typing.lower().split('/'))

