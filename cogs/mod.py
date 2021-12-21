import discord
from discord import member
from discord import channel
from discord.ext import commands
import datetime
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.context import MenuContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.model import ContextMenuType
import re
import requests
import json

guild_ids = [814374218602512395, 829615142450495601]
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

owner_perm = {
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

staff_perm = {
	829615142450495601:[ #bd 
	create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(573896617082748951, SlashCommandPermissionType.USER, True),
	create_permission(829615142450495608, SlashCommandPermissionType.ROLE, True),
	create_permission(829615142450495607, SlashCommandPermissionType.ROLE, True),
	create_permission(829615142450495603, SlashCommandPermissionType.ROLE, True),
	],
	814374218602512395:[ #india
	create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(573896617082748951, SlashCommandPermissionType.USER, True),
	create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
	create_permission(814405684581236774, SlashCommandPermissionType.ROLE, True),
	create_permission(816595613230694460, SlashCommandPermissionType.ROLE, True),
	],
}

mute_perm = {
	814374218602512395:
	[
		create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
		create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
		create_permission(814405684581236774, SlashCommandPermissionType.ROLE, True),
	]
}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)


class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def is_server_staff():
		async def predicate(ctx):
			if ctx.author == ctx.guild.owner: return True
			staff_roleID = [886551491744264222, 814405582177435658,814483202860908564,894123602918670346,892089910528462919,814405684581236774,816595613230694460]
			for role in ctx.author.roles:
				if role.id in staff_roleID:
					return True
				else:
					await ctx.send("Your not allowed to this",hidden=True)
		return commands.check(predicate)


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@cog_ext.cog_slash(name="Mute", description="Put User in timeout", default_permission=False, permissions=mute_perm, guild_ids=[814374218602512395],
		options=[create_option(name="user", description="Select user", option_type=6, required=True),
		create_option(name="time", description="set time max 28days", required=False, option_type=3),
		create_option(name="reason", description="reason of timeout", required=False, option_type=3)])
	async def timeout(self, ctx, user: discord.Member, time: TimeConverter, reason: str=None):
		time = await TimeConverter().convert(ctx, time)
		print(time)
		if int(time) > 2419200:return await ctx.send("You can't set timeout for more than 28days", hidden=True)
		timeout = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
		timeout = timeout.isoformat()

		payload = {
            "communication_disabled_until": timeout
            }
		headers = {
    		"Authorization": f"Bot {self.bot.config_token}",
    		"Content-Type": "application/json",
    		}

		r = requests.patch(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', data=json.dumps(payload),headers=headers)
		await ctx.send("Muted successfully", hidden=True)
		embed = discord.Embed(description=f"<:dynosuccess:898244185814081557> ***{user} Was Timeout*** | {reason}",color=0x11eca4)
		await ctx.channel.send(embed=embed)
		log_embed = discord.Embed(title=f"Mute | {user}")
		log_embed.add_field(name="User", value=user.mention)
		log_embed.add_field(name="Moderator", value=ctx.author.mention)
		log_embed.add_field(name="Reason", value=reason or "None")
		channel = self.bot.get_channel(814461938997788703)
		await channel.send(embed=log_embed)


	@cog_ext.cog_slash(name="config", description="change configuration of server", guild_ids=guild_ids, default_permission=False,permissions=owner_perm,options=[
		create_option(name="general", description="select general channel for your server",required=False, option_type=7),
		create_option(name="eng_chat", description="select english-chat channel for your server",required=False, option_type=7),
		create_option(name="faq", description="select faq channel for your server",required=False, option_type=7),
		create_option(name="news", description="select news channel for your server",required=False, option_type=7),
		create_option(name="language", description="change language for /lang command",required=False, option_type=3),
		create_option(name="bot_channel", description="set channel for bot command", required=False, option_type=7)
		]
	)
	async def config(self, ctx, general: discord.TextChannel=None, eng_chat:discord.TextChannel=None, faq: discord.TextChannel=None, news:discord.TextChannel=None, language: str=None, bot_channel: discord.TextChannel =None):
		if ctx.author.guild_permissions.administrator or ctx.author.id == 488614633670967307:
			
			data = await self.bot.config.find(ctx.guild.id)
			if data is None:
				data = {"_id": ctx.guild.id}

			if general:
				data['general'] = general.id
			if eng_chat:
				data['eng_chat'] = eng_chat.id
			if faq:
				data['faq'] = faq.id
			if news:
				data['new'] = news.id
			if language:
				data['lang'] = language
			if bot_channel:
				if bot_channel.id in data['bot_channel']:
					data['bot_channel'].remove(bot_channel.id)
				if not bot_channel.id in data['bot_channel']:
					data['bot_channel'].append(bot_channel.id)

			await self.bot.config.upsert(data)

			await ctx.send("Server config updated\nNew commands is coming where you can see your configs",hidden=True)
		else:
			await ctx.send("You need `administrator` permissions to use this command")
				
	@cog_ext.cog_slash(name="vote", description="Get vote link of the server", guild_ids=[814374218602512395])
	async def vote(self, ctx):
		guild = self.bot.get_guild(888085276801531967)
		emoji = await guild.fetch_emoji(912764847891025960)
		buttons = [create_button(style=ButtonStyle.URL, label="Top.gg", emoji=emoji, disabled=False, url="https://top.gg/servers/814374218602512395/vote")]
		await ctx.send("You can vote for the server from the link given below.", components=[create_actionrow(*buttons)], hidden=True)


def setup(bot):
	bot.add_cog(Config(bot))