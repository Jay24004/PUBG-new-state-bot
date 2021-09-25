import discord
from discord.ext import commands
import datetime
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
guild_ids = [814374218602512395, 829615142450495601,819267038614519869,777033462086762516,885802388001288262]

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
    ],
    819267038614519869:[
	create_permission(819306312889925632, SlashCommandPermissionType.ROLE, True),
	create_permission(819267811549118505, SlashCommandPermissionType.ROLE, True),
	],
	777033462086762516:[
	create_permission(777033462086762519, SlashCommandPermissionType.ROLE, True),
	],
	885802388001288262:[
	create_permission(885814181549457418, SlashCommandPermissionType.ROLE,True),
	create_permission(885815298110918666, SlashCommandPermissionType.ROLE,True),
	create_permission(888409306616168560, SlashCommandPermissionType.ROLE,True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True)
	]
}

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@cog_ext.cog_slash(name="config", description="change configuration of server", guild_ids=guild_ids, default_permission=False,permissions=owner_perm,options=[
		create_option(name="general", description="select general channel for your server",required=False, option_type=7),
		create_option(name="eng_chat", description="select english-chat channel for your server",required=False, option_type=7),
		create_option(name="faq", description="select faq channel for your server",required=False, option_type=7),
		create_option(name="news", description="select news channel for your server",required=False, option_type=7),
		create_option(name="language", description="change language for /lang command",required=False, option_type=3)
		]
	)
	async def config(self, ctx, general: discord.TextChannel=None, eng_chat:discord.TextChannel=None, faq: discord.TextChannel=None, news:discord.TextChannel=None, language: str=None):
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

			await self.bot.config.upsert(data)

			await ctx.send("Server config updated\nNew commands is coming where you can see your configs",hidden=True)
		else:
			await ctx.send("You need `administrator` permissions to use this command")


def setup(bot):
	bot.add_cog(Config(bot))