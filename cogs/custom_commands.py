import discord
from discord.ext import commands
import datetime
import random
import asyncio
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

guild_ids=[829615142450495601]


staff_perm = {
	829615142450495601:[
	create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(573896617082748951, SlashCommandPermissionType.USER, True),
	create_permission(829615142450495608, SlashCommandPermissionType.ROLE, True),
	create_permission(829615142450495607, SlashCommandPermissionType.ROLE, True),
	create_permission(829615142450495603, SlashCommandPermissionType.ROLE, True),
	]

}

class Misc(commands.Cog):
	def __init__(self , bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Has been loaded")


	@cog_ext.cog_slash(name="avoid", description="when someone chatting off-topic",guild_ids=guild_ids, default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select user to reply", option_type=3,required=True),
		]
	)
	async def avoid(self, ctx, user: str):
		await ctx.channel.send(f"Please avoid going off topic, {user}. You can have unrelated conversations in <#829615143124992020> or <#829615143124992023>")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="say", description="simple say command",guild_ids=guild_ids, default_permission=False, permissions=staff_perm,
		options=[create_option(name="str", description="Type Thing that bot need to send", option_type=3, required=True)]
		)
	async def say(self, ctx, str:str):
		await ctx.channel.send(f"{str}")
		await ctx.send("Said",hidden=True)

	@cog_ext.cog_slash(name="pin", guild_ids=guild_ids, description="refer someone to channel pin message",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),
		]
	)
	async def pin(self, ctx, user: str):
		await ctx.channel.send(f"Please refer to this channel's pinned messages for further information, {user}\n▪︎PC: Click on the pin icon located in the top-right of the channel.\n▪︎ Mobile: Click on the channel name and select Pins located at the top.")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="faq", guild_ids=guild_ids, description="refer someone to faq channel",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),
		]
	)
	async def faq(self, ctx, user: str):
		await ctx.channel.send(f"Please refer to <#829615142672531462> for further information, {user}. Make sure to read through the channel before asking questions in the support channels, as your questions could have been answered there.")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="lang", guild_ids=guild_ids, description="When someone uses other than English or Bangla",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),
		]
	)
	async def lang(self, ctx, user: str):
		await ctx.channel.send(f"Please do not use any other language aside from Bangla and English in this channel. {user}")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="eng", guild_ids=guild_ids, description="When someone uses other than English in general-eng",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),])
	async def eng(self, ctx, user: str):
		await ctx.channel.send(f"Please do not use any other language aside from English in this channel. {user}")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="news", guild_ids=guild_ids, description="When someone ask for New State News",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),])
	async def news(self, ctx, user: str):
		await ctx.channel.send(f"{user} , Keep your eyes on <#882539911310368779> or follow **PUBG : NEW STATE** official social media accounts for the latest news.")
		await ctx.send("done",hidden=True)	


def setup(bot):
	bot.add_cog(Misc(bot))
