from time import strftime

import discord
import os
import random
import logging


from discord.ext import commands
from dotenv import load_dotenv

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

@bot.command()
async def test(ctx):
    await ctx.send('blank')

# Run bot
# Initialize bot with intents


logging.basicConfig(level=logging.INFO)
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)

