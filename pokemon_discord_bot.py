from operator import index

from encodings.aliases import aliases

import discord
import type_calculator
import os
import random
import logging
import embed_builder
import moves_service

from databases import abilitiesDb, movesDb, pokemonDb, itemsDb, conditionsDb, naturesDb, initialize_dbs
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



@bot.command(help = "Check if the bot is awake.", cog_name = "utility")
async def ping(ctx):
    await ctx.send('pong')


@bot.command(help = "Input a name to show the stats of a pokemon.")
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

@bot.command(help = "Input a list of types.", name = "typechart")
async def types_chart(ctx, *, args):
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


@bot.command(help = "Input a name to show the description of a condition.")
async def condition(ctx, *, arg):
    condition = conditionsDb.getCondition(arg)
    if condition is not None:
        await ctx.send(embed = embed_builder.conditionInfo(condition))
    else:
        await ctx.send(f'"{arg}" is not a recognised condition.')


@bot.command(help = "Input a name to show the description of an item.")
async def item(ctx, *, arg):
    item = itemsDb.getItem(arg)
    if item is not None:
        await ctx.send(embed = embed_builder.itemInfo(item))
    else:
        await ctx.sent(f'"{arg}" is not a recognised item.')


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
        await ctx.send(embed = embed_builder.contestInfo(move))
    else:
        await ctx.sent(f'"{arg}" is not a recognised move.')

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


@bot.command(help= "Input a name to show the description of a nature.")
async def nature(ctx, *, arg):
    nature = naturesDb.getNature(arg)
    if nature is not None:
        await ctx.send(embed = embed_builder.natureInfo(nature))
    else:
        await ctx.sent(f'"{arg}" is not a recognised nature.')


@bot.command(help = "evaluate a maths expression.")
async def calc(ctx, *, arg):
    answer = calculate(arg)
    await ctx.send(f'```{arg} = {answer}```')


@bot.command(help = "roll dice. 2d6 = roll a d6 twice.", aliases = ["r"])
async def roll(ctx, arg="20d600"):
    index_of_d = arg.lower().index('d')
    modifier = 0
    if '+' in arg:
        arg, modifier = arg.split("+",1)
    if index_of_d == 0:
        await ctx.send(random.randint(1, int(arg[index_of_d + 1:]))+int(modifier))
    else:
        output = []
        for x in range(int(arg[:index_of_d])):
            output.append(random.randint(1, int(arg[index_of_d + 1:]))+int(modifier))
        str_output = str(output)
        str_output = str_output[1:-1]
        await ctx.send(str_output)


@bot.command(help = "Input a pokemon and a level(optional).")
async def strongestattacks(ctx, *, args):
    if "," in args:
        pokemon_name, level = args.split(',', 1)
        level = int(level)
    else:
        pokemon_name = args
        level = 4
    pokemon = pokemonDb.getPokemon(pokemon_name)
    highestBapMoves = moves_service.calculate_strongest_attacks(pokemon, level)
    embed = embed_builder.strongestAttacksInfo(pokemon, level, highestBapMoves)
    await ctx.send(embed = embed)


@bot.command(help = "Input two pokemon and a level(optional).")
async def seattacks(ctx, *, args):
    count = args.count(",")
    if count == 0:
        await ctx.send("seAttacks takes 2 comma seperated pokemon names, and an optional comma seperated level")
        return
    elif count == 1:
        attacker, defender = args.split(',', 1)
        level = 4
    else:
        attacker, defender, level = args.split(',', 2)
        level = int(level)
    attacker = pokemonDb.getPokemon(attacker)
    defender = pokemonDb.getPokemon(defender)
    sortedSeAttacksByType = moves_service.calculate_se_attacks(attacker, defender, level)
    embed = embed_builder.seAttacksInfo(attacker, defender, sortedSeAttacksByType, level)

    await ctx.send(embed = embed)


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
    embed1 = embed_builder.seAttacksInfo(pokemon1, pokemon2, sortedSeAttacksByType1, level)

    embed2 = embed_builder.seAttacksInfo(pokemon2, pokemon1, sortedSeAttacksByType2, level)

    await ctx.send(embed = embed1)
    await ctx.send(embed = embed2)


# Run bot
# Initialize bot with intents


logging.basicConfig(level=logging.INFO)
initialize_dbs()
start_db_refresher()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)
