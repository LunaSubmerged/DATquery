from itertools import filterfalse

import discord
from numpy.array_api import empty

import moves_service
import type_calculator


# region POKEMON


def pokemonInfo(pokemon):
    if pokemon is not None:
        embed = discord.Embed(
            color = discord.Color.dark_teal(),
            title = pokemon.name,
            description = pokemon.typing
        )
        embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
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
            _move_types = moves_service.count_moves_by_category(pokemon)
            embed.add_field(name=f'Moves - {sum(_move_types)}', value = f'({_move_types[0]} Phys | {_move_types[1]} Spec | {_move_types[2]} Other)', inline=False)
            all_moves = pokemon.getMoves()
            all_moves.sort(key= lambda x: len(x.pokemon_list))
            embed.add_field(name="Rarest Moves", value = f'{all_moves[0].name} ({len(all_moves[0].pokemon_list)}), {all_moves[1].name} ({len(all_moves[1].pokemon_list)}), {all_moves[2].name} ({len(all_moves[2].pokemon_list)})', inline=False)
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
        embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
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
        embed.add_field(name="FE Distribution", value = len(move.pokemon_list))
        embed.add_field(name="Level", value = move.level)
        embed.add_field(name="Combo Level", value = move.combo_lvl)
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
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
    if learn_level == -1:
        embed.description = f"{pokemon.name} does not learn {move.name}."
    else:
        embed.description = f"{pokemon.name} learns {move.name} at level {learn_level}."

    return embed

def move_pokemon_list(moves):
    moves_pokemon_lists = [move.pokemon_list for move in moves]
    shared_pokemon_list = set.intersection(*[set(pokemon_list) for pokemon_list in moves_pokemon_lists])
    embed = discord.Embed(
        color=discord.Color.dark_teal(),
        title=f'Who Learns {", ".join(move.name for move in moves)} ({len(shared_pokemon_list)} Total)'

    )


    pokemon_name_list = [pokemon.name for pokemon in shared_pokemon_list]
    pokemon_name_list.sort()
    embed.description = ', '.join(pokemon_name_list)
    return embed


def can_combo(pokemon, move_1, move_2):
    required_level = max(move_1.level, move_2.level)
    reasons = []
    if not move_1 in pokemon.getMoves():
        reasons.append(f'{pokemon.name} does not learn {move_1.name}.')
    if not move_2 in pokemon.getMoves():
        reasons.append(f'{pokemon.name} does not learn {move_2.name}.')
    if move_1.combo_lvl == "Banned":
        reasons.append(f'{move_1.name} is banned.')
    if move_2.combo_lvl == "Banned":
        reasons.append(f'{move_2.name} is banned.')
    if move_1.combo_lvl == "One" and move_2.combo_lvl == "One":
        reasons.append(f'both moves are c.level one.')

    _color = discord.Color.dark_teal()
    if reasons:
        _color = discord.Color.red()
    embed = discord.Embed(
            color=_color,
            title= f'{pokemon.name} {move_1.name} + {move_2.name} Combo'

    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
    if reasons:
        description = f'{move_1.name} + {move_2.name} is not a legal combo for {pokemon.name} because:\n - {"\n - ".join(reasons)}'
    else:
        description = f'{pokemon.name} learns {move_1.name}+{move_2.name} at level {required_level}.'
    embed.description = description
    return embed

def contestInfo(move):
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
        embed.add_field(name="\u1CBC", value="")
        embed.add_field(name="Appeal", value= move.appeal)
        embed.add_field(name="Jam", value= move.jam)
        embed.add_field(name="\u1CBC", value="")
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
        embed.add_field(name="FE Distribution", value=len(ability.pokemon_list), inline=False)
        return embed

def ability_pokemon_list(abilities):
    ability_pokemon_lists = [ability.pokemon_list for ability in abilities]
    shared_pokemon_list = set.intersection(*[set(pokemon_list) for pokemon_list in ability_pokemon_lists])
    embed = discord.Embed(
        color=discord.Color.dark_teal(),
        title=f'Who has {", ".join(ability.name for ability in abilities)} ({len(shared_pokemon_list)} Total)'

    )


    pokemon_name_list = [pokemon.name for pokemon in shared_pokemon_list]
    pokemon_name_list.sort()
    embed.description = ', '.join(pokemon_name_list)
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

    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
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
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + attacker.showdown_alias + ".png")
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

def typeAttacksInfo(pokemon, type_name, sorted_type_attacks, level):
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = f"{pokemon.name} {type_name} Attacks At Level {level}",
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
    body = ", ".join(move.name for move in sorted_type_attacks)
    embed.add_field(name = type_name, value = body)

    return embed

def priorityAttacksInfo(pokemon, priority_moves, level):
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = f"{pokemon.name} Priority Attacks At Level {level}",
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
    body = ", ".join(move.name for move in priority_moves)
    embed.add_field(name = "Moves", value = body)

    return embed
# endregion

# region TYPES
def type_intensity_dict (types_chart):
    weak = ""
    resist = ""
    immunity = ""
    for type in type_calculator.typesDictionary.keys():
        local_type = types_chart[type_calculator.typesDictionary[type]]
        if local_type == 2:
            weak += ", " + type.capitalize()
        elif local_type > 2:
            weak += f", **{type.capitalize()} (X{local_type })**"
        elif local_type == 0:
            immunity += ", " + type.capitalize()
        elif local_type == 0.5:
            resist += ", " + type.capitalize()
        elif local_type <= 0.25:
            resist += f", **{type.capitalize()} (X{local_type })**"
    weak = weak[1:]
    resist = resist[1:]
    immunity = immunity[1:]
    local_type_chart_dict = {
        "weak" : weak,
        "resist" : resist,
        "immunity" : immunity
    }
    return local_type_chart_dict


def pokemon_weak_embed(pokemon):
    types_list = type_calculator.get_type_chart_pokemon(pokemon)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = pokemon.name,
        description = pokemon.typing
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.showdown_alias + ".png")
    _type_intensity_dict = type_intensity_dict(types_list)
    embed.add_field(name="Weaknesses", value = _type_intensity_dict["weak"])
    embed.add_field(name="Resistances", value = _type_intensity_dict["resist"], inline= False)
    embed.add_field(name="Immunities", value = _type_intensity_dict["immunity"], inline= False)

    return embed


def defensive_types_chart_embed(types_list):
    types_defence_chart = type_calculator.get_types_defense_chart(types_list)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = "Defensive Type Chart",
        description = "/".join([pokemon_type.capitalize() for pokemon_type in types_list])
    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/bastiodon.png")
    _type_intensity_dict = type_intensity_dict(types_defence_chart)
    embed.add_field(name="Weaknesses", value=_type_intensity_dict["weak"])
    embed.add_field(name="Resistances", value=_type_intensity_dict["resist"], inline=False)
    embed.add_field(name="Immunities", value=_type_intensity_dict["immunity"], inline=False)

    return embed


def offensive_types_chart_embed(types_list):
    types_offence_chart = type_calculator.get_types_offense_chart(types_list)
    embed = discord.Embed(
        color = discord.Color.dark_teal(),
        title = "Offensive Type Chart",
        description = "/".join([pokemon_type.capitalize() for pokemon_type in types_list])
    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/rampardos.png")
    _type_intensity_dict = type_intensity_dict(types_offence_chart)
    embed.add_field(name="Weaknesses", value=_type_intensity_dict["weak"])
    embed.add_field(name="Resistances", value=_type_intensity_dict["resist"], inline=False)
    embed.add_field(name="Immunities", value=_type_intensity_dict["immunity"], inline=False)

    return embed


# endregion

# region UTILITY

def links():
    embed = discord.Embed(
        color=discord.Color.dark_teal(),
        title="Helpful Links"
    )
    embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/bw/" + "rotom" + ".png")
    _quick_access = "[Quick Ref](https://www.smogon.com/forums/threads/3724806/)"
    _realgam = "[Realgam](https://www.smogon.com/forums/threads/3712853/)"
    _subway = "[Subway](https://www.smogon.com/forums/threads/3763303/)"
    _safari = "[Safari](https://www.smogon.com/forums/threads/3725044/)"
    _raid = "[Raid](https://www.smogon.com/forums/threads/3725186/)"
    _guild = "[Guild](https://www.smogon.com/forums/threads/3758090/)"
    _battle_tree = "[Battle Tree](https://www.smogon.com/forums/threads/3736347/)"
    _pike = "[Pike](https://www.smogon.com/forums/threads/3748229/)"
    _boasts = "[Boasting Hall](https://www.smogon.com/forums/threads/3728546/)"
    _getting_started = "[Getting Started](https://www.smogon.com/forums/threads/3708940/)"
    _comp_rules = "[Comp Rules](https://www.smogon.com/forums/threads/3708940/post-9355888)"
    _substitutions = "[Substitutions](https://www.smogon.com/forums/threads/3708940/#post-9368457)"
    _action_groups = "[Action Groups](https://www.smogon.com/forums/threads/3708940/#-10-6)"
    _main_page = "[BBP Forum](https://www.smogon.com/forums/forums/164/)"
    _DAT = "[DAT](https://docs.google.com/spreadsheets/d/1qIplFdrzRqHl91V7qRBtsb9LuC1TYW--TFoNlTDvpbA/edit?gid=825844183#gid=825844183)"
    _combo_finder = "[Profile Maker/Combo Finder](https://docs.google.com/spreadsheets/d/1KuqXxwczBg_1X__K4z0uG5nImm2l5Q3VM0PPVcAsjKM/edit)"
    _first_order_guide = "[HAF Guide To First Ordering](https://www.smogon.com/forums/threads/3697025/page-16#post-10237123)"
    _move_highlighting_guide = "[HAF Move Highlighting Guide](https://www.smogon.com/forums/threads/3697025/page-15#post-10068511)"
    _reffing_guide = "[Duo Reffing Guide](https://www.smogon.com/forums/threads/3697025/post-10316439)"

    embed.add_field(name="Rule Book", value=f"{_getting_started}\n{_comp_rules}\n{_substitutions}\n{_action_groups}")
    embed.add_field(name = "Data", value =f"{_quick_access}\n{_realgam}\n{_subway}\n{_safari}\n{_raid}\n{_guild}\n{_battle_tree}\n{_pike}\n{_boasts}")
    embed.add_field(name="\u1CBC", value = "\u1CBC", inline= False)
    embed.add_field(name="Tools", value=f"{_main_page}\n{_DAT}\n{_combo_finder}")
    embed.add_field(name="Community Guides", value=f"{_first_order_guide}\n{_move_highlighting_guide}\n{_reffing_guide}")
    return embed
#endregion