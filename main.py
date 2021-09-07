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
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio
from amari import AmariClient

from discord.ext import commands
from pathlib import Path
from discord_slash import SlashCommand
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
# Local code
import utils.json_loader

from utils.mongo import Document
from utils.util import Pag
from utils.util import clean_code

load_dotenv()
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


intents = discord.Intents.all()  # Help command requires member intents
DEFAULTPREFIX = "!"
bot = commands.Bot(
    description="commands List of Me",
    command_prefix=">",
    case_insensitive=True,
    owner_ids=[391913988461559809, 488614633670967307, 301657045248114690],
    intents=intents,
)
slash = SlashCommand(bot, sync_commands=False, sync_on_cog_reload=True)
DiscordComponents(bot)
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
bot.version = "4.1"
bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: None\n-----")
    await bot.change_presence(status=discord.Status.offline)

    currentGive = await bot.give.get_all()
    for give in currentGive:
        bot.giveaway[give["_id"]] = give

    print("Database Connected\n-----")

@bot.event
async def on_command_error(error, ctx):
    return

@bot.command(hidden=True)
@commands.is_owner()
async def amari(ctx, user:discord.Member=None):
    user = user if user else ctx.author

    amari = AmariClient(bot.amari)

    amari_level = await amari.fetch_user(ctx.guild.id, user.id)

    await ctx.send(f"User Name: `{user.display_name}'\nAmari Level: {amari_level.level}\nWeekly Amari: {amari_level.weeklyexp}")

@slash.context_menu(target=ContextMenuType.MESSAGE,
                    name="whois",
                    guild_ids=[829615142450495601])
async def whois(ctx: MenuContext):
    def fomat_time(time):
        return time.strftime('%d-%B-%Y %I:%m %p')

    member = ctx.target_message.author
    usercolor = member.color

    today = (datetime.datetime.utcnow() - member.created_at).total_seconds()

    embed = discord.Embed(title=f'{member.name}', color=usercolor)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='Account Name:', value=f'{member.name}', inline=False)
    embed.add_field(name='Created at:', value=f"{fomat_time(member.created_at)}\n{format_timespan(today)}")
    embed.add_field(name='Joined at', value=fomat_time(member.joined_at))
    embed.add_field(name='Account Status', value=str(member.status).title())
    embed.add_field(name='Account Activity', value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None")

    hsorted_roles = sorted([role for role in member.roles[-2:]], key=lambda x: x.position, reverse=True)


    embed.add_field(name='Top Role:', value=', '.join(role.mention for role in hsorted_roles), inline=False)
    embed.add_field(name='Number of Roles', value=f"{len(member.roles) -1 }")
    embed.set_footer(text=f'ID {member.id}', icon_url=member.avatar_url)
    await ctx.send(embed=embed, hidden=True)

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["tgk_database"]
    bot.config = Document(bot.db, "config")
    bot.give = Document(bot.db, "giveaway")

    
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_") and not file.startswith("slash"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)
