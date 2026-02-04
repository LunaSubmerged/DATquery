from time import strftime

import discord
import os
import random
import logging
import databases
import embed_builder
import moves_service

from databases import abilitiesDb, movesDb, pokemonDb, itemsDb, conditionsDb, initialize_dbs, disciplineDb
from dotenv import load_dotenv
from discord.ext import commands
from calculator import calculate
from db_refresher import start_db_refresher

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category = "Commands")
load_dotenv()
command_prefix = os.environ.get("COMMAND_PREFIX")
bot = commands.Bot(command_prefix= command_prefix, intents=intents, help_command=help_command)


@bot.event
async def on_ready():
    logging.info("Bot is ready.")


@bot.command(help = "Return when the bot was last updated.")
async def updated(ctx):
    await ctx.send(f"last updated {strftime("%H:%M:%S, %x", databases.last_refresh_time)}.")

@bot.command(help = "link the rule book", aliases=["rule"])
async def rules(ctx, arg = "index"):
    _error = "input must be in the form number1.number2"
    if arg == "index":
        await ctx.send("https://www.smogon.com/forums/threads/battle-by-post-player-handbook-generation-9.3708940/post-9355888")
    elif "." in arg:
        int1, int2 = arg.split(".")
        int1 = ''.join(filter(str.isdigit,int1))
        int2 = ''.join(filter(str.isdigit,int2))
        await ctx.send(f"<https://www.smogon.com/forums/threads/.3708940/#-{int1}-{int2}>")
    else:
        await ctx.send(_error)

@bot.command(help = "Check if the bot is awake.", cog_name = "utility")
async def ping(ctx):
    await ctx.send('pong')

@bot.command(help = "Link faq channel.", cog_name = "utility")
async def faq(ctx):
    await ctx.send('You can find our FAQ here: <#1295726153977565256>')

@bot.command(help = "Helpful links", aliases = ["link", "l"])
async def links(ctx):
    await  ctx.send(embed = embed_builder.links())

@bot.command(help = "Input a name to show the stats of a pokemon.", aliases = ["pokemon","dex","mon"])
async def stats(ctx, *, arg):
    pokemon = pokemonDb.getPokemon(arg)
    if pokemon is not None:
        await ctx.send(embed = embed_builder.pokemonInfo(pokemon))
    else:
        await ctx.send(f'"{arg}" is not a recognised pokemon.')


@bot.command(help = "Input a name to show the type chart of a pokemon.")
async def weak(ctx, *, arg):
    pokemon = pokemonDb.getPokemon(arg)
    if pokemon is not None:
        await ctx.send(embed = embed_builder.pokemon_weak_embed(pokemon))
    else:
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command(help = "Input a list of types.", name = "typechart", aliases = ["type", "types", "typeschart"])
async def type_chart(ctx, *, args):
    types_list = [pokemon_type.strip() for pokemon_type in args.split(',')]
    if types_list is not None:
        await ctx.send(embed=embed_builder.offensive_types_chart_embed(types_list))
        await ctx.send(embed = embed_builder.defensive_types_chart_embed(types_list))
    else:
        await ctx.send(f'"{args}" is not a recognised string of types.')

@bot.command(help = "Input a name to show the types of a pokemon.", name="pokemontypes")
async def pokemon_types(ctx, *, arg):
    pokemon = pokemonDb.getPokemon(arg)
    if pokemon is not None:
        await ctx.send(embed = embed_builder.pokemonTypes(pokemon))
    else:
        await ctx.send(f'"{arg}" is not a recognised pokemon.')


@bot.command(help = "Input a name to show the description of an ability.")
async def ability(ctx, *, arg):
    ability = abilitiesDb.getAbility(arg)
    if ability is not None:
        await ctx.send(embed = embed_builder.abilityInfo(ability))
    else:
        await ctx.send(f'"{arg}" is not a recognised ability.')

@bot.command(help = "Input a list of abilities.", aliaes = ["hasabilities", "whohas"])
async def hasability(ctx, *, input_ability_names):
    ability_names = input_ability_names.split(',')
    abilities = [abilitiesDb.getAbility(ability_name) for ability_name in ability_names]
    embed = embed_builder.ability_pokemon_list(abilities)
    await ctx.send(embed=embed)


@bot.command(help = "Input a name to show the description of a condition.", aliases = ["status"])
async def condition(ctx, *, arg):
    condition = conditionsDb.getCondition(arg)
    if condition is not None:
        await ctx.send(embed = embed_builder.conditionInfo(condition))
    else:
        await ctx.send(f'"{arg}" is not a recognised condition.')


@bot.command(help = "Input a name to show the description of an item.")
async def item(ctx, *, arg):
    item = itemsDb.get_item(arg)
    if item is not None:
        await ctx.send(embed = embed_builder.item_info(item))
    else:
        await ctx.sent(f'"{arg}" is not a recognised item.')

@bot.command(help = "Input a name to show the description of a discipline.")
async def discipline(ctx, *, arg):
    discipline = disciplineDb.get_discipline(arg)
    if discipline is not None:
        await ctx.send(embed = embed_builder.discipline_info(discipline))
    else:
        await ctx.sent(f'"{arg}" is not a recognised discipline.')

@bot.command(help= "Input a name to show the description of a move.")
async def move(ctx, *, arg):
    move = movesDb.getMove(arg)
    if move is not None:
        await ctx.send(embed = embed_builder.moveInfo(move))
    else:
        await ctx.sent(f'"{arg}" is not a recognised move.')


@bot.command(help= "Input a name to show the description of a move.")
async def contest(ctx, *, arg):
    move = movesDb.getMove(arg)
    if move is not None:
        await ctx.send(embed = embed_builder.contest_info(move))
    else:
        await ctx.sent(f'"{arg}" is not a recognised move.')

@bot.command(help = "Input the name of a tag.", aliases = ["tags"])
async def tag(ctx, *, tag_name):
    cleaned_tag_name = "#" + tag_name.capitalize()
    tagged_moves = list(filter(lambda _move: cleaned_tag_name in _move.tags, movesDb.dictionary.values()))
    if len(tagged_moves) == 0:
        await ctx.send("could not find any moves with that tag")
    else:
        embed = embed_builder.tagged_moves(tag_name, tagged_moves)
        await ctx.send(embed = embed)

@bot.command(help = "Input the name of a pokemon and a tag.", aliases = ["montag, ptag"])
async def pokemontag(ctx, *, args):
    count = args.count(",")
    level = 4

    if count == 1:
        pokemon_name, tag_name = args.split(',', 1)
    else:
        pokemon_name, tag_name, level = args.split(',', 2)
        level = int(level)
    pokemon = pokemonDb.getPokemon(pokemon_name)
    cleaned_tag_name = "#" + tag_name.strip().capitalize()
    tagged_moves = list(filter(lambda _move: cleaned_tag_name in _move.tags, pokemon.get_moves_level(level)))
    if len(tagged_moves) == 0:
        await ctx.send("could not find any moves with that tag")
    else:
        embed = embed_builder.pokemon_tagged_moves(cleaned_tag_name, tagged_moves, pokemon, level)
        await ctx.send(embed = embed)

@bot.command(help= "Input a pokemon and a move.")
async def learn(ctx, *, args):
    if "," in args:
        pokemon_name, move_name = args.split(',', 1)
        pokemon = pokemonDb.getPokemon(pokemon_name)
        move = movesDb.getMove(move_name)
        embed = embed_builder.learn_move_info(pokemon, move)
        await ctx.send(embed=embed)
    else:
        await ctx.sent("That was not correctly formated. Input should be pokemon , move")

@bot.command(help = "input a move to see who learns it.", aliases = ["canlearn", "arns", "wholearns", "learns"])
async def knows(ctx, *, input_move_names):
    move_names = input_move_names.split(',')
    moves = [movesDb.getMove(move_name) for move_name in move_names]
    embed = embed_builder.move_pokemon_list(moves)
    await ctx.send(embed=embed)

@bot.command(help = "Input a pokemon and 2 moves.", aliases = ["cancombo"])
async def combo(ctx, *, args):
    if args.count(",") == 2:
        pokemon_name, move_1_name, move_2_name = args.split(',', 2)
        pokemon = pokemonDb.getPokemon(pokemon_name)
        move_1 = movesDb.getMove(move_1_name)
        move_2 = movesDb.getMove(move_2_name)
        embed = embed_builder.can_combo(pokemon, move_1, move_2)
        await ctx.send(embed=embed)
    else:
        await ctx.sent("That was not correctly formated. Input should be pokemon, move, move")

@bot.command(help = "Evaluate a maths expression.")
async def calc(ctx, *, arg):
    answer = calculate(arg)
    await ctx.send(f'```{arg} = {answer}```')


@bot.command(help = "Roll dice. 2d6 = roll a d6 twice.", aliases = ["r"])
async def roll(ctx, arg="20d600"):
    index_of_d = arg.lower().index('d')
    modifier = 0
    if '+' in arg:
        arg, modifier = arg.split("+",1)
        modifier = int(modifier)
    elif '-' in arg:
        arg, modifier = arg.split("-", 1)
        modifier = -int(modifier)
    if index_of_d == 0:
        await ctx.send(random.randint(1, int(arg[index_of_d + 1:]))+modifier)
    else:
        output = []
        for x in range(int(arg[:index_of_d])):
            output.append(random.randint(1, int(arg[index_of_d + 1:]))+modifier)
        str_output = str(output)
        str_output = str_output[1:-1]
        await ctx.send(f"```{str_output}```")


@bot.command(help = "Input a pokemon and a level(optional).", aliases = ["attacks"])
async def strongestattacks(ctx, *, args):
    if "," in args:
        pokemon_name, level = args.split(',', 1)
        level = int(level)
    else:
        pokemon_name = args
        level = 4
    pokemon = pokemonDb.getPokemon(pokemon_name)
    highestBapMoves = moves_service.calculate_strongest_attacks(pokemon, level)
    embed = embed_builder.strongest_attacks_info(pokemon, level, highestBapMoves)
    await ctx.send(embed = embed)


@bot.command(help = "Input two pokemon and a level(optional).")
async def seattacks(ctx, *, args):
    count = args.count(",")
    if count == 0:
        await ctx.send("seattacks takes 2 comma separated pokemon names, and an optional comma separated level")
        return
    elif count == 1:
        attacker, defender = args.split(',', 1)
        level = 4
    else:
        attacker, defender, level = args.split(',', 2)
        level = int(level)
    attacker = pokemonDb.getPokemon(attacker)
    defender = pokemonDb.getPokemon(defender)
    sorted_se_attacks_by_type = moves_service.calculate_se_attacks(attacker, defender, level)
    embed = embed_builder.se_attacks_info(attacker, defender, sorted_se_attacks_by_type, level)

    await ctx.send(embed = embed)

@bot.command(help = "Input a pokemon, a type and a level(optional).")
async def typeattacks(ctx, *, args):
    count = args.count(",")
    if count == 0:
        await ctx.send("typeattacks takes a comma separated pokemon name and a type, with an optional comma separated level")
        return
    elif count == 1:
        pokemon, pokemon_type = args.split(',', 1)
        level = 4
    else:
        pokemon, pokemon_type, level = args.split(',', 2)
        level = int(level)
    pokemon = pokemonDb.getPokemon(pokemon)
    type_name = pokemon_type.strip().capitalize()
    sorted_type_attacks = moves_service.calculate_typed_attacks(pokemon, type_name, level)
    embed = embed_builder.typeAttacksInfo(pokemon, type_name, sorted_type_attacks, level)
    await ctx.send(embed=embed)

@bot.command(help = "Input a name to show the priority moves of a pokemon.")
async def priority(ctx, *, args):
    count = args.count(",")
    if count == 0:
        pokemon_name = args
        level = 4
    else:
        pokemon_name, level_str = args.split(',', 1)
        level = int(level_str)
    pokemon = pokemonDb.getPokemon(pokemon_name)
    if pokemon is not None:
        priority_moves = filter(lambda move: int(move.priority) > 0, pokemon.get_moves())
        priority_moves = filter(lambda move: int(move.level) <= level, priority_moves)
        embed = embed_builder.priorityMovesInfo(pokemon, priority_moves, level)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'"{args}" is not a recognised pokemon.')


@bot.command(help = "Input two pokemon and a level(optional).")
async def matchup(ctx, *, args):
    count = args.count(",")
    if count == 0:
        await ctx.send("seAttacks takes 2 comma seperated pokemon names, and an optional comma seperated level")
        return
    elif count == 1:
        pokemon1_name, pokemon2_name = args.split(',', 1)
        level = 4
    else:
        pokemon1_name, pokemon2_name, level = args.split(',', 2)
        level = int(level)

    pokemon1 = pokemonDb.getPokemon(pokemon1_name)
    pokemon2 = pokemonDb.getPokemon(pokemon2_name)
    sortedSeAttacksByType1 = moves_service.calculate_se_attacks(pokemon1, pokemon2, level)
    sortedSeAttacksByType2 = moves_service.calculate_se_attacks(pokemon2, pokemon1, level)
    embed1 = embed_builder.se_attacks_info(pokemon1, pokemon2, sortedSeAttacksByType1, level)

    embed2 = embed_builder.se_attacks_info(pokemon2, pokemon1, sortedSeAttacksByType2, level)

    await ctx.send(embed = embed1)
    await ctx.send(embed = embed2)

@bot.command(help = "Return boss immunities", aliases = ["immunity", "boss"])
async def bossimmunity(ctx):
    await ctx.send(embed=embed_builder.conditionInfo(conditionsDb.getCondition("boss immunity")))
# Run bot
# Initialize bot with intents


logging.basicConfig(level=logging.INFO)
initialize_dbs()
start_db_refresher()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)
