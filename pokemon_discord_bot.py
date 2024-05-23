import discord
import type_calculator
import os
import pokemon
import random

from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category = "Commands")
bot = commands.Bot(command_prefix='%', intents=intents, help_command=help_command)
db = pokemon.PokemonDatabase()


@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.listen("on_message")
async def on_message(message):
    if message.content == "ping":
        await message.channel.send("pong")
@bot.command(help = "Check if the bot is awake.", cog_name = "utility")
async def ping(ctx):
    await ctx.send('pong')

@bot.command(help = "Input a name to show the stats of a pokemon.")
async def stats(ctx, arg):
    pokemon = db.getPokemon(arg)
    if pokemon != None:
      await ctx.send(embed = db.pokemonInfo(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command(help = "Input a name to show the type chart of a pokemon.")
async def weak(ctx, arg):
    pokemon = db.getPokemon(arg)
    if pokemon != None:
      await ctx.send(embed = type_calculator.typeNum(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command()
async def calc(ctx, arg):
    await ctx.send(float(arg))

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



# Run bot
# Initialize bot with intents
load_dotenv()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)

