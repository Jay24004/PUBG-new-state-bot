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

from humanfriendly import format_timespan
import utils.json_loader
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType,ButtonStyle
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, create_button, wait_for_component
from discord_slash.context import ComponentContext

from discord.ext import commands

description = "Some Basic commands"

staff_perm = {
    814374218602512395:[
    create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
    create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
    create_permission(573896617082748951, SlashCommandPermissionType.USER, True)
    ],
    829615142450495601:[
    create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
    create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
    create_permission(573896617082748951, SlashCommandPermissionType.USER, True)
    ]
}

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

    @cog_ext.cog_slash(name="ping", description="show bots latency",guild_ids=None)
    async def ping(self, ctx):
        start_time = time.time()
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
                              description=f"**Response TIme** {round(self.bot.latency * 1000)}ms\n**Database Ping**: {round(dping * 1000)}Ms\n**My Age**: {format_timespan(total_s)}")

        await ctx.send(content=None, embed=embed)

    @cog_ext.cog_slash(
        name="stats", description="A useful command that displays bot statistics.",guild_ids=None
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        main_guild = self.bot.get_guild(814374218602512395)
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

        code = main_guild.get_member(488614633670967307)
        eng1 = main_guild.get_member(567374379575672852)
        eng2 = main_guild.get_member(573896617082748951)
        embed.add_field(name="Bot's Maintainers:",
                        value=f"**Developer**: {code.mention}\n**Writers**{eng1.mention},{eng2.mention}")
        embed.set_footer(
            text=f"Developed by Jay | {self.bot.user.name}",icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed, delete_after=60)
    
    @cog_ext.cog_slash(name="help", description="help command for your help", guild_ids=None, default_permission=False, permissions=staff_perm)
    async def help(self, ctx):

        timestamp = datetime.datetime.utcnow()
        main_embed = discord.Embed(title=f"Help Command",
            description=f"This is the help command for the {self.bot.user.mention}\nYou can see the list of all modules below, some may not be available on your server.\n\n**Modules:**\n\n**Basic:**\n> Most basic commands of the bot, which shows the information about the bot or the bot's new updates.\n\n**Infomation Commands:**\n> The purpose of these commands are mostly to give server members information about the server or the game.\n\n**Giveaways**:\n> This giveaway method are a little bit advanced, which can set role requirement or rank level requirement. (Currently only Amari Bot levels requirement is available, mee6 levels requirement is coming very soon)\n\n**Reddit:**\n> Brings up Reddit contents. This module is currently available in PUBG: New State Bangladesh\n\n**Mini-Games:**\n> This module has some mini-games including tic-tac-toe, rock paper scissors, etc. This module is currently available in PUBG: New State Bangladesh ",color=0x2f3136)
        main_embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        main_embed.timestamp = timestamp

        basic_embed = discord.Embed(title="Basic Commands", description=f"These Commands are the basic commands to show the bot's ping, server count, total users, etc.\n\n**__Commands:__**\n\n**1. /ping** \n> Shows the bot's latency.\n\n**2. /stats**\n> An useful command that displays the bot's statistics.",color=0x2f3136)
        basic_embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        basic_embed.timestamp = timestamp

        info_embed = discord.Embed(title="Information Commands", description="These Commands can be used to give server members information about the server or the game.\n\n__**Commands**__\n\n**1. /avoid**\n> When someone is chatting off-topic.\n> Example: /avoid user: @user#1234\n\n**2. /say**\n> Send a message by the bot.\n> Example: /say str: message\n\n**3. /pin**\n> Refer someone to channel pin message.\n> Example: /pin user: @user#1234\n\n**4. /faq**\n> Refer someone to the server's faq channel.\n> Example: /faq user: @user#1234\n\n**5. /lang**\n> When someone uses a language other than the allowed ones.\n> Example: /lang user: @user#1234\n\n**6. /eng**\n> When someone uses other than English in English channel.\n>  Example: /eng user: @user#1234\n\n**7. /news**\n> Refer someone to server news channel\n> Example: /news user: @user#123\n\nNote: you can enter multiple users in same commands",color=0x2f3136)
        info_embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        info_embed.timestamp = timestamp

        giveaway_embed = discord.Embed(title="Giveaway Commands", description="Server admins can create Giveaways with this bot which can have different requirements.\n\n**__Commands__**\n\n**1. /gstart**\n> Start the Giveaway.\n ㅤ ",color=0x2f3136)
        giveaway_embed.add_field(name="Required  Options", value="**◽ time**\n>  How long the giveaway should last (must be atleast 15 seconds)\n\n**◽ price**\n> The price of the giveaway\n\n**◽ winners**\n>  Number of the winners", inline=True)
        giveaway_embed.add_field(name=" ㅤ ", value=" ㅤ ", inline=True)
        giveaway_embed.add_field(name="Optional Options", value="**◽ required_role**\n> Required role to join the giveaway\n\n**◽ bypass_role**\n> With this role users can bypass any requirements of that giveaway\n\n**◽ amari_level**\n> Set required amari level\n\n**◽ weekly_amari**\n> set giveaway weekly amari", inline=True)
        giveaway_embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        giveaway_embed.timestamp = timestamp

        giveaway_embed2 = discord.Embed(title="Giveaway Commands",description="**2. /gend**\n> Force end a giveaway\n> Example: /gend message_id: message_id of giveaway\n\n**3. /greroll**\n> Reroll the giveaway for new winners\n> Example: /greroll channel: channel of giveaway message_id: message id of the giveaway winners: numbers of winners\n\n**4. /gdelete**\n> Delete a giveaway\n> Example: /gdelete message_id:  message id of the giveaway channel: channel of giveaway\n\n**5. /setblacklist**\n> Blacklist role from giveaway it\'s a Server-wide blacklist\n> Example: /setblacklist role: role mention \n\n**6. /setbypass**\n> Set role to bypass all server giveaway\nExample: /setbypass role: role mention \n\n**7. /bypasslist**\n> Send the Bypass role list\n\n**8. /blacklist**\n> Send the Blacklist role list", color=0x2f3136)
        giveaway_embed2.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        giveaway_embed2.timestamp = timestamp

        select = create_select(placeholder="Select your Page Here",options=
                    [
                    create_select_option(label="Main Page", value="1", emoji="🗂️"),
                    create_select_option(label="Basic Commands", value="2", emoji="📖"),
                    create_select_option(label="Infomation Commands", value="3", emoji="ℹ️"),
                    create_select_option(label="Giveaways-1", value="4", emoji="🎉"),
                    create_select_option(label="Giveaways-2", value="5", emoji="🎉")]
        )
        msg = await ctx.send(embed=main_embed, components=[create_actionrow(select)], hidden=True)
        while True:
            try:
                def custom_check(component_ctx: ComponentContext) -> bool:
                    if component_ctx.author == ctx.author:
                        return True
                res: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(select)], check=custom_check, timeout=60)
                if int(res.selected_options[0]) == 1:
                    await res.edit_origin(embed=main_embed, components=[create_actionrow(select)])
                if int(res.selected_options[0]) == 2:
                    await res.edit_origin(embed=basic_embed, components=[create_actionrow(select)])
                if int(res.selected_options[0]) == 3:
                    await res.edit_origin(embed=info_embed, components=[create_actionrow(select)])
                if int(res.selected_options[0]) == 4:
                    await res.edit_origin(embed=giveaway_embed, components=[create_actionrow(select)])
                if int(res.selected_options[0]) == 5:
                    await res.edit_origin(embed=giveaway_embed2, components=[create_actionrow(select)])

            except asyncio.TimeoutError:
                break


def setup(bot):
    bot.add_cog(Basic(bot))
