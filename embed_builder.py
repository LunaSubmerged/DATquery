import discord
import moves_service
import type_calculator


# region POKEMON


def pokemon_info(pokemon):
    if pokemon is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = pokemon.name,
            description = pokemon.typing
        )
        embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
        embed.add_field(name="Abilities", value = pokemon.abilities)
        if pokemon.hidden_ability != "":
            embed.add_field(name="Hidden Ability", value = pokemon.hidden_ability)
        line1 = "HP: " + pokemon.hp
        line2 = "ATK: " + pokemon.atk + " | DEF: " + pokemon.defence + " | SpA: " + pokemon.sp_a + " | SpD: " + pokemon.sp_d
        line3 = "Speed: " + pokemon.spe
        line4 = "Size Class: " + pokemon.size
        line5 = "Weight Class: " + pokemon.weight
        embed.add_field(name="Stats", value = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5, inline= False)
        if pokemon.movesList is not None:
            _move_types = moves_service.count_moves_by_type(pokemon)
            embed.add_field(name=f'Moves - {sum(_move_types)}', value = f'({_move_types[0]} Phys | {_move_types[1]} Spec | {_move_types[2]} Other)', inline=False)
        if pokemon.signature_move != "":
            embed.add_field(name="Signature Move", value = pokemon.signature_move, inline=False)
        if pokemon.traits != "":
            embed.add_field(name="Traits", value = pokemon.traits)

        return embed


def pokemon_types(pokemon):
    if pokemon is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = pokemon.name,
            description = pokemon.typing
        )
        embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    return (embed)

def showdown_search_pokemon(pokemon_name_list):

    embed = discord.Embed(
        color=discord.Color.dark_teal(),
        title= "Showdown Search Pokemon",
        description="\n".join(pokemon_name_list)
    )

    return embed
def showdown_search_moves(move_list):

    embed = discord.Embed(
        color=discord.Color.dark_teal(),
        title= "Showdown Search Moves",
        description="\n".join(move_list)
    )

    return embed

# endregion


# region MOVES

def move_info(move):
    if move is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = move.name,
            description = f"*{move.fluff}*"
        )
        if move.description != "":
            if len(move.description) <= 1024:
                embed.add_field(name="Description", value=move.description, inline=False)
            else:
                embed.add_field(name = "Description", value="This move is too long, go look it up in the DAT.", inline=False)
        embed.add_field(name="Category", value = move.category)
        embed.add_field(name="Type", value = move.type)
        embed.add_field(name="Accuracy", value = move.acc)
        embed.add_field(name="BAP", value= move.bap)
        embed.add_field(name="Energy Cost", value=move.en_cost)
        embed.add_field(name="Target", value= move.target)
        embed.add_field(name="Effect Chance", value= move.effect)
        embed.add_field(name="Priority", value= move.priority)
        embed.add_field(name="Tags", value= move.tags)
        embed.add_field(name="\u1CBC", value = f'Contact: {move.contact}')
        embed.add_field(name="\u1CBC", value = f'Reflect: {move.reflect}')
        embed.add_field(name="\u1CBC", value = f'Snatch: {move.snatch}')


    return embed

def learn_move_info(pokemon, move):
    learn_level = -1
    color = discord.Color.red()
    for level, level_moves in enumerate(pokemon.movesList):
        if move in level_moves:
            learn_level = level
            color = discord.Color.dark_teal()
            break

    embed = discord.Embed(
        color=color,
        title=pokemon.name

    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    if learn_level == -1:
        embed.description = f"{pokemon.name} does not learn {move.name}."
    else:
        embed.description = f"{pokemon.name} learns {move.name} at level {learn_level}."

    return embed

# endregion


# region ABILITIES

def contest_info(move):
    if move is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = move.name,
            description = f"*{move.contest_fluff}*"
        )
        if move.contest_description != "":
            embed.add_field(name="Description", value=move.contest_description, inline=False)
        embed.add_field(name="Tags", value= move.tags)
        embed.add_field(name="Genre", value= move.genre)
        embed.add_field(name="Appeal", value= move.appeal)
        embed.add_field(name="Jam", value= move.jam)
    return embed

# endregion


# region CONDITIONS

def ability_info(ability):
    if ability is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = ability.name,
            description = f"*{ability.fluff}*"
        )
        if len(ability.description) <= 1024:
            embed.add_field(name = "Description", value = ability.description)
        else:
            embed.add_field(name = "Description", value="This ability is too long, go look it up in the DAT.")
        return embed

# endregion


# region ITEMS

def condition_info(condition):
    if condition is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = condition.name,
            description = f"*{condition.fluff}*"
        )
        embed.add_field(name = "Description", value = condition.description, inline=False)
        embed.add_field(name = "Default Duration", value = condition.default_duration)
        return embed

# endregion


# region NATURES

def item_info(item):
    if item is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = item.name,
            description = f"*{item.fluff}*"
        )
        embed.add_field(name = "Description", value = item.description, inline=False)
        return embed

# endregion


# region ATTACKS

def nature_info(nature):
    if nature is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = nature.name,
            description = nature.description
        )
        return embed


def strongest_attacks_info(pokemon, level, highestBapMoves):
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = pokemon.name,
        description = f"Highest BAP moves, adjusted for {pokemon.name}'s attack stats at level {level}.\n attack = {pokemon.atk}, spA = {pokemon.sp_a}"
    )

    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    noAttacks = []
    for key in highestBapMoves:
        if highestBapMoves[key] is not None:
            name = key.title()
            if name in pokemon.typing:
                name = f"{name}(STAB)"
            embed.add_field(name = name, value = highestBapMoves[key].name)
        else:
            noAttacks.append(key.title())
    noAttacksStr = ", ".join(noAttacks)
    embed.add_field(name="No Attacks", value = noAttacksStr)
    return embed


def se_attacks_info(attacker, defender, sortedSeAttacksByType, level):
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = f"{attacker.name} VS {defender.name}",
        description = f"SE moves, for {attacker.name} vs {defender.name} at level {level}. \n attack = {attacker.atk}, spA = {attacker.sp_a}, def = {defender.defence}, spD = {defender.sp_d}"
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + attacker.sprite_alias + ".png")
    localTypeChart = type_calculator.get_type_chart_pokemon(defender)
    for moveType in sortedSeAttacksByType:
        name = moveType.title()
        if name in attacker.typing:
            name = f"{name}(STAB)"

        if localTypeChart[type_calculator.typesDictionary[moveType]] >= 4:
            name = f"{name}(4X)"
        sortedStr = ", ".join([move.name for move in sortedSeAttacksByType[moveType]])
        embed.add_field(name = name, value = sortedStr)

    return embed
# endregion

# region TYPES
def pokemon_weak_embed(pokemon):
    typesList = type_calculator.get_type_chart_pokemon(pokemon)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = pokemon.name,
        description = pokemon.typing
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    weak = ""
    resist = ""
    immunity = ""
    for type in type_calculator.typesDictionary.keys():
        localType = typesList[type_calculator.typesDictionary[type]]
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

    return embed


def defensive_types_chart_embed(types_list):
    types_defence_chart = type_calculator.get_types_defense_chart(types_list)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = "Defensive Type Chart",
        description = "/".join([pokemon_type.capitalize() for pokemon_type in types_list])
    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/bastiodon.png")
    weak = ""
    resist = ""
    immunity = ""
    for pokemon_type in type_calculator.typesDictionary.keys():
        local_type = types_defence_chart[type_calculator.typesDictionary[pokemon_type]]
        if local_type == 2:
            weak += ", " + pokemon_type.capitalize()
        elif local_type >= 4:
            weak += ", **" + pokemon_type.capitalize() + "**"
        elif local_type == 0:
            immunity += ", " + pokemon_type.capitalize()
        elif local_type == 0.5:
            resist += ", " + pokemon_type.capitalize()
        elif local_type <= 0.25:
            resist += ", **" + pokemon_type.capitalize() + "**"
    weak = weak[1:]
    resist = resist[1:]
    immunity = immunity[1:]
    embed.add_field(name="Weaknesses", value = weak)
    embed.add_field(name="Resistances", value = resist, inline= False)
    embed.add_field(name="Immunities", value = immunity, inline= False)

    return embed


def offensive_types_chart_embed(types_list):
    types_offence_chart = type_calculator.get_types_offense_chart(types_list)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = "Offensive Type Chart",
        description = "/".join([pokemon_type.capitalize() for pokemon_type in types_list])
    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/rampardos.png")
    weak = ""
    resist = ""
    immunity = ""
    for pokemon_type in type_calculator.typesDictionary.keys():
        local_type = types_offence_chart[type_calculator.typesDictionary[pokemon_type]]
        if local_type == 2:
            weak += ", " + pokemon_type.capitalize()
        elif local_type >= 4:
            weak += ", **" + pokemon_type.capitalize() + "**"
        elif local_type == 0:
            immunity += ", " + pokemon_type.capitalize()
        elif local_type == 0.5:
            resist += ", " + pokemon_type.capitalize()
        elif local_type <= 0.25:
            resist += ", **" + pokemon_type.capitalize() + "**"
    weak = weak[1:]
    resist = resist[1:]
    immunity = immunity[1:]
    embed.add_field(name="Super Effective", value = weak)
    embed.add_field(name="Resisted", value = resist, inline= False)
    embed.add_field(name="Immuned", value = immunity, inline= False)

    return embed


# endregion