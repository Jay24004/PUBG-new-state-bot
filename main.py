# Standard libraries
import contextlib
import io
import logging
import os
from dotenv import load_dotenv

# Third party librariesimport textwrap
import datetime
import discord
import json
import motor.motor_asyncio

from humanfriendly import format_timespan
from traceback import format_exception
import asyncio
from amari import AmariClient

from discord.ext import commands
from pathlib import Path
from discord_slash import SlashCommand
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
# Local code
import utils.json_loader

from utils.mongo import Document
from utils.util import Pag
from utils.util import clean_code

load_dotenv()
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


staff_perm = {
    829615142450495601:[
    create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
    create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
    create_permission(829615142450495609, SlashCommandPermissionType.ROLE, True),
    create_permission(829615142450495608, SlashCommandPermissionType.ROLE, True),
    create_permission(829615142450495607, SlashCommandPermissionType.ROLE, True),
    create_permission(829615142450495603, SlashCommandPermissionType.ROLE, True)
    ]

}


intents = discord.Intents.all()  # Help command requires member intents
DEFAULTPREFIX = "!"
bot = commands.Bot(
    description="commands List of Me",
    command_prefix=">",
    case_insensitive=True,
    owner_ids=[391913988461559809, 488614633670967307, 301657045248114690],
    intents=intents,
)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
# change command_prefix='-' to command_prefix=get_prefix for custom prefixes
bot.config_token = str(os.getenv('TOKEN'))
bot.connection_url = str(os.getenv('MONGO'))
bot.amari = str(os.getenv('AMARI'))

logging.basicConfig(level=logging.INFO)

bot.muted_users = {}
bot.ban_users = {}
bot.blacklist_user = {}
bot.guild_id = [797920317871357972]
bot.ticket_setups = {}
bot.cwd = cwd
bot.event_channel = {}
bot.perm = {}
bot.giveaway = {}
bot.mod_role = [797923152617275433, 848585998769455104]
bot.version = "0.5"
bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: None\n-----")
    await bot.change_presence(status=discord.Status.dnd)

    currentGive = await bot.give.get_all()
    for give in currentGive:
        bot.giveaway[give["_id"]] = give

    print("Database Connected\n-----")

#@bot.event
#async def on_command_error(error, ctx):
    #return

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension: str):
    bot.load_extension(f'cogs.{extension}')

    await ctx.send(f'The {extension} is successfully Loaded.')

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension: str):
    bot.unload_extension(f'cogs.{extension}')

    await ctx.send(f'The {extension} is successfully unloaded.')


@bot.command(hidden=True)
@commands.is_owner()
async def amari(ctx, user:discord.Member=None):
    user = user if user else ctx.author

    amari = AmariClient(bot.amari)

    amari_level = await amari.fetch_user(ctx.guild.id, user.id)

    await ctx.send(f"User Name: `{user.display_name}'\nAmari Level: {amari_level.level}\nWeekly Amari: {amari_level.weeklyexp}")

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["tgk_database"]
    bot.config = Document(bot.db, "config")
    bot.give = Document(bot.db, "giveaway")
    bot.score = Document(bot.db, "score")

    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_") and not file.startswith("slash") and not file.startswith("test"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)
