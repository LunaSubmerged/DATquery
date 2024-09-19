import discord
import type_calculator
# region POKEMON


def pokemonInfo(pokemon):
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
        if pokemon.signature_move != "":
            embed.add_field(name="Signature Move", value = pokemon.signature_move, inline=False)
        if pokemon.traits != "":
            embed.add_field(name="Traits", value = pokemon.traits)

        return (embed)


def pokemonTypes(pokemon):
    if pokemon is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = pokemon.name,
            description = pokemon.typing
        )
        embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    return (embed)

# endregion


# region MOVES

def moveInfo(move):
    if move is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = move.name,
            description = f"*{move.fluff}*"
        )
        if move.description != "":
            embed.add_field(name="Description", value=move.description, inline=False)
        embed.add_field(name="Category", value = move.category)
        embed.add_field(name="Type", value = move.type)
        embed.add_field(name="Accuracy", value = move.acc)
        embed.add_field(name="BAP", value= move.bap)
        embed.add_field(name="Energy Cost", value=move.en_cost)
        embed.add_field(name="Target", value= move.target)
        embed.add_field(name="Effect Chance", value= move.effect)
        embed.add_field(name="Priority", value= move.priority)
        embed.add_field(name="Tags", value= move.tags)
        embed.add_field(name="Additional Info", value = f'Contact: {move.contact} \n Reflect: {move.reflect}')
        embed.add_field(name="\u1CBC", value = f'Snatch: {move.snatch}')

    return embed


def contestInfo(move):
    if move is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = move.name,
            description = f"*{move.contest_fluff}*"
        )
        if move.description != "":
            embed.add_field(name="Description", value=move.contest_description, inline=False)
        embed.add_field(name="Tags", value= move.tags)
        embed.add_field(name="Genre", value= move.genre)
        embed.add_field(name="Appeal", value= move.appeal)
        embed.add_field(name="Jam", value= move.jam)
    return embed

# endregion


# region ABILITIES

def abilityInfo(ability):
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


# region CONDITIONS

def conditionInfo(condition):
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


# region ITEMS

def itemInfo(item):
    if item is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = item.name,
            description = f"*{item.fluff}*"
        )
        embed.add_field(name = "Description", value = item.description, inline=False)
        return embed

# endregion


# region NATURES

def natureInfo(nature):
    if nature is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = nature.name,
            description = nature.description
        )
        return embed

# endregion


# region ATTACKS

def strongestAttacksInfo(pokemon, level, highestBapMoves):
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


def seAttacksInfo(attacker, defender, sortedSeAttacksByType, level):
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = f"{attacker.name} VS {defender.name}",
        description = f"SE moves, for {attacker.name} vs {defender.name} at level {level}. \n attack = {attacker.atk}, spA = {attacker.sp_a}, def = {defender.defence}, spD = {defender.sp_d}"
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + attacker.sprite_alias + ".png")
    localTypeChart = type_calculator.getTypeChart(defender)
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
