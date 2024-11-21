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


class PaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 5
    data : []

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title=f"User List Page {self.current_page} / {int(len(self.data) / self.sep) + 1}")
        for item in data:
            embed.add_field(name=item['label'], value=item['item'], inline=False)
        return embed

    async def update_message(self,data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if not self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="|<",
                       style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<",
                       style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">",
                       style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|",
                       style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep) + 1
        await self.update_message(self.get_current_page_data())


class Button(discord.ui.View):
    @discord.ui.button(label="Button", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        await interaction.response.edit_message(content = self.message_2, view = None)


@bot.event
async def on_ready():
    logging.info("Bot is ready.")

@bot.command(help = "Check if the bot is awake.", cog_name = "utility")
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def test(ctx):
    data = [

    ]

    for i in range(1, 15):
        data.append({
            "label": "User Event",
            "item": f"User {i} has been added"
        })

    pagination_view = PaginationView(timeout=None)
    pagination_view.data = data

    await pagination_view.send(ctx)

# Run bot
# Initialize bot with intents


logging.basicConfig(level=logging.INFO)
discord_token = os.environ.get("DISCORD_TOKEN")
bot.run(discord_token)

