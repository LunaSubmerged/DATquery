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

typechart =  [
        [1,2,1,1,0.5,0.5,0.5,0.5,0.5,2,1,1,1,0.5,2,1,0.5,1],
        [1,0.5,1,1,0.5,0.5,1,1,2,1,1,1,1,1,2,1,1,1],
        [1,1,2,1,0,1,1,1,1,1,1,1,1,1,1,1,0.5,1],
        [1,1,0.5,0.5,1,1,1,2,1,0.5,0,1,1,1,1,1,1,2],
        [1,2,2,1,1,2,0.5,1,1,1,1,1,1,0.5,1,1,0.5,1],
        [0.5,2,1,1,0.5,1,1,0.5,0,1,1,2,2,0.5,0.5,2,2,1],
        [2,1,0.5,1,1,1,0.5,1,1,2,1,2,1,1,1,0.5,2,0.5],
        [2,1,1,0.5,1,2,1,1,1,2,1,1,1,1,1,0.5,0.5,1],
        [1,0.5,1,1,1,1,1,1,2,1,1,1,0,1,2,1,1,1],
        [0.5,1,0.5,1,1,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,2],
        [0.5,1,1,2,1,1,2,0,1,0.5,1,1,1,2,1,2,2,1],
        [1,1,2,1,1,1,0.5,2,1,2,2,0.5,1,1,1,1,0.5,0.5],
        [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0.5,0.5,1],
        [1,1,1,1,2,1,1,1,0.5,2,0.5,1,1,0.5,1,0.5,0,1],
        [1,0,1,1,1,2,1,1,1,1,1,1,1,2,0.5,1,0.5,1],
        [2,1,1,1,1,0.5,2,2,1,1,0.5,2,1,1,1,1,0.5,1],
        [1,1,1,0.5,2,1,0.5,1,1,1,1,2,1,1,1,2,0.5,0.5],
        [1,1,0.5,1,1,1,2,1,1,0.5,2,1,1,1,1,2,1,0.5]
    ]

def typeNum(pokemon):
    typesList = []
    for i in range(len(typesDictionary)):
        typesList.append(1)

    for type in typesDictionary.keys():
        if type in pokemon.typing.lower():
            tempList = list(typesList)
            typesList.clear()
            for count, value in enumerate(typechart):
                print(value)
                print(value[typesDictionary[type]])
                typesList.append(value[typesDictionary[type]] * tempList[count])
                

    return typesList