import datetime
import discord
import random
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
        num = random.randint(1,2)
        if num == 1:
            member = len(set(self.bot.get_all_members()))
            activity = f'over {member} Players'
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity),status=discord.Status.dnd)
        if num == 2:
            activity = "New update /update"
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=activity),status=discord.Status.dnd)

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = await self.bot.config.find(488614633670967307)
        if guild.id in data['white_list']:
            data = {"_id": guild.id, "general": None,"eng_chat": None,"faq": None,"new": None,"lang": None, "g_bypass":[], "g_blacklist": []}
            await self.bot.config.upsert(data)
            return
        else:
            try:
                await guild.owner.send(f"Someone try to add me to your server `{guild.name} | {guild.id}`, but your server is not in whitelist i left the server\nif you think there is an probelm DM `JAY#0138`")
            except discord.HTTPException:
                pass
            await guild.leave()
            owner = await self.bot.fetch_user(488614633670967307)
            await owner.send(f"I was Added to Name: {guild.name} | ID: {guild.id}\n As it's not WhiteListed i left")
            
    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, ex):
        if isinstance(ex, commands.MissingPermissions):
            await ctx.send("Hey! You lack permission to use this command.")
        elif isinstance(ex, commands.MissingAnyRole):
           await ctx.send("Hey! You lack permission to use this command.")
        elif isinstance(ex, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(ex.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f" You must wait {int(s)} seconds to use this command!",hidden=True)
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f" You must wait {int(m)} minutes and {int(s)} seconds to use this command!",hidden=True
                )
            else:
                await ctx.send(
                    f" You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!",hidden=True
                )
        else:
            embed = discord.Embed(color=0xE74C3C, 
                description=f"Error: `{ex}`")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))