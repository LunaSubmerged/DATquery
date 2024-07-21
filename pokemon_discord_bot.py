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
import constants
import type_calculator


from io import StringIO
from dotenv import load_dotenv
from discord.ext import commands
from calculator import calculate
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from type_calculator import typesDictionary

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category = "Commands")
load_dotenv()
command_prefix = os.environ.get("COMMAND_PREFIX")
bot = commands.Bot(command_prefix= command_prefix, intents=intents, help_command=help_command)
movesDb = moves.MoveDatabase()
pokemonDb = pokemon.PokemonDatabase()
abilitiesDb = abilities.AbilityDatabase()
conditionsDb = conditions.ConditionDatabase()
itemsDb = items.ItemDatabase()
naturesDb = natures.NatureDatabase()
databases = [abilitiesDb, movesDb,pokemonDb,itemsDb, conditionsDb, naturesDb]

def attachMoves():
    data = requests.get(constants.MOVE_POOL)
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

def effectiveBap(move, pokemon):
    _return = 0
    if move.category != "Other" and move.bap != "??" and move.bap != "--":
        if (move.category == "Physical"):
            if(move.bap == "6 or 11"):
                _return = 6 + int(pokemon.atk)
            else:    
                _return = int(move.bap) +  int(pokemon.atk)
        else:
            _return = int(move.bap) + int(pokemon.sp_a)
    return int(_return)

def relativeEffectiveBap(move, pokemon1, pokemon2):
    _return = 0
    if move.category != "Other" and move.bap != "??" and move.bap != "--":
        if (move.category == "Physical"):
            if(move.bap == "6 or 11"):
                _return = 6 + int(pokemon1.atk) - int(pokemon2.defence)
            else:    
                _return = int(move.bap) +  int(pokemon1.atk) - int(pokemon2.defence)
        else:
            _return = int(move.bap) + int(pokemon1.sp_a) - int(pokemon2.sp_d)
    return int(_return)

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
      await ctx.send(embed = type_calculator.typeNumEmbed(pokemon))
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

@bot.command(help = "show the best attacks for a pokemon. Optional level parameter, for example 'ghastly, 2' would return the best moves of each type that ghastly knows at level 2.")
async def strongestAttacks(ctx,*,args):
    if "," in args:
        pokemon, level = args.split(',', 1)
        level = int(level)
    else:
        pokemon = args
        level = 4
    pokemon = pokemonDb.getPokemon(pokemon)
    moves = []
    for n in range(level + 1):
        moves = moves + pokemon.movesList[n]
    highestBapMoves = {}
    for pokemonType in typesDictionary:
        highestBapMoves[pokemonType] = None
    for move in moves:
        comparitor = highestBapMoves[move.type.lower()]
        if(not move.category == "Other") and (not move.bap == "??") and (not "deals fixed damage" in move.description) and (comparitor == None or effectiveBap(comparitor, pokemon) < effectiveBap(move,pokemon)):              
            highestBapMoves[move.type.lower()] = move
    embed = discord.Embed(
    color = discord.Color.dark_teal(),
    title = pokemon.name,
    description = f"Highest BAP moves, adjusted for {pokemon.name}'s attack stats at level {level}."
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon.sprite_alias + ".png")
    noAttacks = []
    for key in highestBapMoves:
        if highestBapMoves[key] != None:
            name = key.title()
            if name in pokemon.typing:
                name = f"{name}(STAB)"
            embed.add_field(name = name, value = highestBapMoves[key].name)
        else:
            noAttacks.append(key.title())
    noAttacksStr = ", ".join(noAttacks)
    embed.add_field(name="No Attacks", value = noAttacksStr)
    await ctx.send (embed = embed)

@bot.command(help = "show the best se attacks for a pokemon vs another pokemon. Optional level parameter, for example 'ghastly, abra, 2' would return the best moves of each se type that ghastly knows at level 2.")
async def seAttacks(ctx,*,args):
    count = args.count(",")
    if count == 0:
        await ctx.send ("seAttacks takes 2 comma seperated pokemon names, and an optional comma seperated level")
        return
    elif count == 1:
        pokemon1, pokemon2 = args.split(',', 1)
        level = 4
    else:
        pokemon1, pokemon2, level = args.split(',', 2)
        level = int(level)
    pokemon1 = pokemonDb.getPokemon(pokemon1)
    pokemon2 = pokemonDb.getPokemon(pokemon2)
    moves = []
    for n in range(level + 1):
        moves = moves + pokemon1.movesList[n]
    highestBapMoves = {}
    for pokemonType in typesDictionary:
        highestBapMoves[pokemonType] = None

    for move in moves:
        comparitor = highestBapMoves[move.type.lower()]
        if(not move.category == "Other") and (not move.bap == "??") and (not "deals fixed damage" in move.description) and (comparitor == None or relativeEffectiveBap(comparitor, pokemon1, pokemon2) < relativeEffectiveBap(move,pokemon1, pokemon2)):              
            highestBapMoves[move.type.lower()] = move
    embed = discord.Embed(
    color = discord.Color.dark_teal(),
    title = f"{pokemon1.name} VS {pokemon2.name}",
    description = f"Best SE moves, for {pokemon1.name} vs {pokemon2.name} at level {level}."
    )
    embed.set_thumbnail(url = "https://play.pokemonshowdown.com/sprites/bw/" + pokemon1.sprite_alias + ".png")
    localTypeChart = type_calculator.getTypeChart(pokemon2)
    for key in highestBapMoves:
        if highestBapMoves[key] != None and localTypeChart[typesDictionary[key]] >= 2:
            name = key.title()
            if name in pokemon1.typing:
                name = f"{name}(STAB)"
            if localTypeChart[typesDictionary[key]] >= 4:
                name = f"{name}(4X)"
            embed.add_field(name = name, value = highestBapMoves[key].name)
    await ctx.send (embed = embed)

# Run bot
# Initialize bot with intents
attachMoves()
logging.basicConfig(level=logging.INFO)
dbRefreshThreads = threading.Thread(target = dbRefreshScheduler)
dbRefreshThreads.start()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)

