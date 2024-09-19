import discord
import type_calculator
import os
import random
import logging
import embed_builder
import attacks_service

from databases import abilitiesDb, movesDb, pokemonDb, itemsDb, conditionsDb, naturesDb, intitialize_dbs
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


@bot.listen("on_message")
async def on_message(message):
    if message.content == "ping":
        await message.channel.send("pong")


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
        await ctx.send(embed = type_calculator.typeNumEmbed(pokemon))
    else:
        await ctx.send(f'"{arg}" is not a recognised pokemon.')


@bot.command(help = "Input a name to show the types of a pokemon.")
async def types(ctx, *, arg):
    pokemon = pokemonDb.getPokemon(arg)
    if pokemon is not None:
        await ctx.send(embed = embed_builder.pokemonTypes(pokemon))
    else:
        await ctx.send(f'"{arg}" is not a recognised pokemon.')


@bot.command(help = "Input a name to show the description of an ability.")
async def ability(ctx, *, arg):
    ability = abilitiesDb.getAbility(arg)
    if ability is not None:
        await ctx.send(embed = abilitiesDb.abilityInfo(ability))
    else:
        await ctx.send(f'"{arg}" is not a recognised ability.')


@bot.command(help = "Input a name to show the description of a condition.")
async def condition(ctx, *, arg):
    condition = conditionsDb.getCondition(arg)
    if condition is not None:
        await ctx.send(embed = conditionsDb.conditionInfo(condition))
    else:
        await ctx.send(f'"{arg}" is not a recognised condition.')


@bot.command(help = "Input a name to show the description of an item.")
async def item(ctx, *, arg):
    item = itemsDb.getItem(arg)
    if item is not None:
        await ctx.send(embed = itemsDb.itemInfo(item))
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
        await ctx.send(embed = movesDb.contestInfo(move))
    else:
        await ctx.sent(f'"{arg}" is not a recognised move.')


@bot.command(help= "Input a name to show the description of a nature.")
async def nature(ctx, *, arg):
    nature = naturesDb.getNature(arg)
    if nature is not None:
        await ctx.send(embed = naturesDb.natureInfo(nature))
    else:
        await ctx.sent(f'"{arg}" is not a recognised nature.')


@bot.command(help = "evaluate a maths expression. Use '**' for exponent instead of '^'")
async def calc(ctx, *, arg):
    answer = calculate(arg)
    if answer.startswith("is not a valid expression."):
        await ctx.send(f'"{arg}" {answer}')
    else:
        await ctx.send(f'{arg} = {answer}')


@bot.command(help = "roll a number of dice in the format xdy, x = number of dice rolled, y = sides of the dice.")
async def roll(ctx, arg):
    index_of_d = arg.lower().index('d')
    if index_of_d == 0:
        await ctx.send(random.randint(1, int(arg[index_of_d + 1:])))
    else:
        output = []
        for x in range(int(arg[:index_of_d])):
            output.append(random.randint(1, int(arg[index_of_d + 1:])))
        str_output = str(output)
        str_output = str_output[1:-1]
        await ctx.send(str_output)


@bot.command(help = "show the best attacks for a pokemon. Optional level parameter, for example 'ghastly, 2' would return the best attacks of each type that ghastly knows at level 2.")
async def strongestAttacks(ctx, *, args):
    if "," in args:
        pokemon_name, level = args.split(',', 1)
        level = int(level)
    else:
        pokemon_name = args
        level = 4
    pokemon = pokemonDb.getPokemon(pokemon_name)
    highestBapMoves = attacks_service.calculateStrongestAttacks(pokemon, level)
    embed = embed_builder.strongestAttacksInfo(pokemon, level, highestBapMoves)
    await ctx.send(embed = embed)


@bot.command(help = "show the se attacks for a pokemon vs another pokemon. Optional level parameter, for example 'ghastly, abra, 2' would return the se attacks that ghastly knows vs abra at level 2.")
async def seAttacks(ctx, *, args):
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
    sortedSeAttacksByType = attacks_service.calculateSeAttacks(attacker, defender, level)
    embed = embed_builder.seAttacksInfo(attacker, defender, sortedSeAttacksByType, level)

    await ctx.send(embed = embed)


@bot.command(help = "show seAttacks for pokemon vs each other")
async def matchUp(ctx, *, args):
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
    sortedSeAttacksByType1 = attacks_service.calculateSeAttacks(pokemon1, pokemon2, level)
    sortedSeAttacksByType2 = attacks_service.calculateSeAttacks(pokemon2, pokemon1, level)
    embed1 = embed_builder.seAttacksInfo(pokemon1, pokemon2, sortedSeAttacksByType1, level)

    embed2 = embed_builder.seAttacksInfo(pokemon2, pokemon1, sortedSeAttacksByType2, level)

    await ctx.send(embed = embed1)
    await ctx.send(embed = embed2)


# Run bot
# Initialize bot with intents


logging.basicConfig(level=logging.INFO)
intitialize_dbs()
start_db_refresher()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)
