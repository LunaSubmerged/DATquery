import discord
import type_calculator
import os
import pokemon
import abilities
import conditions
import moves
import items
import random
import schedule
import time
import threading
import logging
import requests
import csv
import natures

from io import StringIO
from dotenv import load_dotenv
from discord.ext import commands
from calculator import calculate

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category = "Commands")
bot = commands.Bot(command_prefix='%', intents=intents, help_command=help_command)
movesDb = moves.MoveDatabase()
pokemonDb = pokemon.PokemonDatabase()
abilitiesDb = abilities.AbilityDatabase()
conditionsDb = conditions.ConditionDatabase()
itemsDb = items.ItemDatabase()
naturesDb = natures.NatureDatabase()
databases = [abilitiesDb, movesDb,pokemonDb,itemsDb, conditionsDb, naturesDb]

def attachMoves():
    data = requests.get("https://docs.google.com/spreadsheets/d/1XDqCQF4miFGGaY5tGTTAgTaZ7koKiqgPAB571fYbVt4/export?format=csv&gid=0")
    csv_file = StringIO(data.text)
    reader = csv.reader(csv_file)
    rows = list(reader)
    start = False
    for row in rows:
        if row[1] == "Pokemon":
            start = True
            continue
        if start:
            pokemonRow = row
            if pokemonRow[4].startswith("No Movepool Data for this species and forme."):
                continue
            
            name = pokemonRow[1]
            level0MoveList = pokemonRow[3].splitlines()
            level1MoveList = pokemonRow[4].splitlines()
            level2MoveList = pokemonRow[5].splitlines()
            level3MoveList = pokemonRow[6].splitlines()
            level4MoveList = pokemonRow[7].splitlines()
            if len(level0MoveList) +  len(level1MoveList) + len(level2MoveList) + len(level3MoveList) + len(level4MoveList) <= 3:
                continue
            pokemon = pokemonDb.getPokemon(name)
            if pokemon.movesList is None:
                level0MoveListFinal = [movesDb.getMove(moveName) for moveName in level0MoveList]
                level1MoveListFinal = [movesDb.getMove(moveName) for moveName in level1MoveList]
                level2MoveListFinal = [movesDb.getMove(moveName) for moveName in level2MoveList]
                level3MoveListFinal = [movesDb.getMove(moveName) for moveName in level3MoveList]
                level4MoveListFinal = [movesDb.getMove(moveName) for moveName in level4MoveList]
                pokemon.movesList = [level0MoveListFinal,level1MoveListFinal,level2MoveListFinal,level3MoveListFinal,level4MoveListFinal]


def dbRefresh():
    for db in databases:
        db.refresh_db()
    attachMoves()



def dbRefreshScheduler():
    schedule.every().day.at("00:00:00").do(dbRefresh)
    while True:
        schedule.run_pending()
        time.sleep(60)



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
    if pokemon != None:
      await ctx.send(embed = pokemonDb.pokemonInfo(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command(help = "Input a name to show the type chart of a pokemon.")
async def weak(ctx, *, arg):
    pokemon = pokemonDb.getPokemon(arg)
    if pokemon != None:
      await ctx.send(embed = type_calculator.typeNum(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command(help = "Input a name to show the types of a pokemon.")
async def types(ctx, *, arg):
    pokemon = pokemonDb.getPokemon(arg)
    if pokemon != None:
      await ctx.send(embed = pokemonDb.pokemonTypes(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command(help = "Input a name to show the description of an ability.")
async def ability(ctx, *,  arg):
    ability = abilitiesDb.getAbility(arg)
    if ability != None:
        await ctx.send(embed = abilitiesDb.abilityInfo(ability))
    else:
        await ctx.send(f'"{arg}" is not a recognised ability.')
@bot.command(help = "Input a name to show the description of a condition.")
async def condition(ctx, *,  arg):
    condition = conditionsDb.getCondition(arg)
    if condition != None:
        await ctx.send(embed = conditionsDb.conditionInfo(condition))
    else:
        await ctx.send(f'"{arg}" is not a recognised condition.')        
@bot.command(help = "Input a name to show the description of an item.")
async def item(ctx, *, arg):
    item = itemsDb.getItem(arg)
    if item != None:
        await ctx.send(embed = itemsDb.ItemInfo(item))
    else:
        await ctx.sent(f'"{arg}" is not a recognised item.')
@bot.command(help= "Input a name to show the description of a move.")
async def move(ctx, *, arg):
    move = movesDb.getMove(arg)
    if move != None:
        await ctx.send(embed = movesDb.moveInfo(move))
    else:
        await ctx.sent(f'"{arg}" is not a recognised move.')
@bot.command(help= "Input a name to show the description of a nature.")
async def nature(ctx, *, arg):
    nature = naturesDb.getNature(arg)
    if nature != None:
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
async def roll(ctx,arg):
    index_of_d = arg.lower().index('d')
    if index_of_d == 0:
        await ctx.send(random.randint(1,int(arg[index_of_d+1:])))
    else:
        output = []
        for x in range(int(arg[:index_of_d])):
            output.append(random.randint(1,int(arg[index_of_d+1:])))
        str_output = str(output)
        str_output = str_output[1:-1]
        await ctx.send(str_output)

@bot.command()
async def test(ctx,*,args):
    if "," in args:
        arg1, arg2 = args.split(',', 1)
        print("arg1 " + arg1)
        print("arg2 " + arg2)
    else:
        print("test command takes 2 pokemon with a comma between their names")

# Run bot
# Initialize bot with intents
attachMoves()
logging.basicConfig(level=logging.INFO)
dbRefreshThreads = threading.Thread(target = dbRefreshScheduler)
dbRefreshThreads.start()
load_dotenv()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)

