import datetime
import discord

from copy import deepcopy
from humanfriendly import format_timespan
from dateutil.relativedelta import relativedelta
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

from discord.ext import tasks, commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count_task = self.change_status.start()

    def cog_unload(self):
        self.count_task.cancel()

    @tasks.loop(seconds=60)
    async def change_status(self):      
        guild = await self.bot.fetch_guild(829615142450495601)
        activity = f'over {len(guild.members)} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"),status=discord.Status.offline)

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    
    #@commands.Cog.listener()
    #async def on_slash_command_error(self, ctx, ex):
    #    if isinstance(ex, commands.MissingPermissions):
    #        await ctx.send("Hey! You lack permission to use this command.")
    #    elif isinstance(ex, commands.MissingAnyRole):
    #       await ctx.send("Hey! You lack permission to use this command.")
    #    else:
    #        embed = discord.Embed(color=0xE74C3C, 
    #            description=f"Error: `{ex}`")
    #        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Events(bot))