import discord
import type_calculator
import os
import pokemon

from dotenv import load_dotenv
from discord.ext import commands




intents = discord.Intents.all()

# Initialize bot with intents
bot = commands.Bot(command_prefix='%', intents=intents)
db = pokemon.PokemonDatabase()
@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.listen("on_message")
async def on_message(message):
    if message.content == "ping":
        await message.channel.send("pong")
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def stats(ctx, arg):
    pokemon = db.getPokemon(arg)
    if pokemon != None:
      await ctx.send(embed = db.pokemonInfo(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command()
async def weak(ctx, arg):
    pokemon = db.getPokemon(arg)
    if pokemon != None:
      await ctx.send(embed = type_calculator.typeNum(pokemon))
    else: 
        await ctx.send(f'"{arg}" is not a recognised pokemon.')

@bot.command()
async def calc(ctx, arg):
    await ctx.send(float(arg))

# Run bot
load_dotenv()
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)

