import asyncio
import discord
import os
from discord.ext.commands import converter
import psutil
import time
import platform
import random
import datetime
import traceback
import datetime
from humanfriendly import format_timespan
import utils.json_loader
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext


from discord.ext import commands

description = "Some Basic commands"
guild_ids=[829615142450495601, 814374218602512395, 819267038614519869]

class Basic(commands.Cog, description=description):
    def __init__(self, bot):
        self.bot = bot

    def is_me():
        def predicate(ctx):
            return ctx.message.author.id in [488614633670967307, 573896617082748951,573896617082748951]
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @is_me()
    async def ping(self, ctx):
        await ctx.message.delete()
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        start = self.bot.uptime
        now = datetime.datetime.utcnow()
        newtime = (now - start)
        total_s = newtime.total_seconds()

        dstart = datetime.datetime.utcnow()
        await self.bot.config.find(ctx.guild.id)
        dend = datetime.datetime.utcnow()
        dping = (dend - dstart)
        dping = dping.total_seconds()

        embed = discord.Embed(title="Pings!", color=ctx.author.colour,
                              description=f"**Response TIme** {round(self.bot.latency * 1000)}ms\n**API**: {round((end_time - start_time) * 1000)}ms\n**Database Ping**: {round(dping * 1000)}Ms\n**My Age**: {format_timespan(total_s)}")

        await message.edit(content=None, embed=embed)

    @cog_ext.cog_slash(
        name="stats", description="A useful command that displays bot statistics.",guild_ids=guild_ids
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        cpu = round(psutil.cpu_percent(), 1)

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            colour=ctx.author.colour,
            timestamp=datetime.datetime.utcnow(),
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="CPU Useage:", value=f"{str(cpu)}%")
        embed.add_field(name="RAM Useage:",
                        value=f"{round(psutil.virtual_memory().percent,1)}%")
        embed.add_field(name="Bot Developers:",
                        value="<@488614633670967307>")
        embed.set_footer(
            text=f"Developed by Jay | {self.bot.user.name}",icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed, delete_after=60)


def setup(bot):
    bot.add_cog(Basic(bot))
