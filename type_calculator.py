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

typeChart =  [
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

def getTypeChart(pokemon):
    typesList = []
    for i in range(len(typesDictionary)):
        typesList.append(1)

    for type in typesDictionary.keys():
        if type in pokemon.typing.lower():
            tempList = list(typesList)
            typesList.clear()
            for count, value in enumerate(typeChart):
                typesList.append(value[typesDictionary[type]] * tempList[count])
    return typesList

def typeNumEmbed(pokemon):
    typesList = getTypeChart(pokemon)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = pokemon.name,
        description = pokemon.typing
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    weak = ""
    resist = ""
    immunity = ""
    for type in typesDictionary.keys():
        localType = typesList[typesDictionary[type]]
        if localType == 2:
            weak += ", " + type.capitalize()
        elif localType >= 4:
            weak += ", **" + type.capitalize() + "**"
        elif localType == 0:
            immunity += ", " + type.capitalize()
        elif localType == 0.5:
            resist += ", " + type.capitalize()
        elif localType <= 0.25:
            resist += ", **" + type.capitalize() + "**"
    weak = weak[1:]
    resist = resist[1:]
    immunity = immunity[1:]    
    embed.add_field(name="Weaknesses", value = weak)
    embed.add_field(name="Resistances", value = resist, inline= False)
    embed.add_field(name="Immunities", value = immunity, inline= False)

    return (embed)