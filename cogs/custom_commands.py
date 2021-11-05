import discord
from discord.ext import commands
import datetime
import random
import asyncio
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
			#bd 				#india			
guild_ids=[829615142450495601, 814374218602512395,]
819267038614519869

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

staff_perm2 = {
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
	]
}

class Misc(commands.Cog):
	def __init__(self , bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@cog_ext.cog_slash(name="avoid", description="when someone chatting off-topic",guild_ids=guild_ids, default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select user to reply", option_type=3,required=True),
		]
	)
	async def avoid(self, ctx, user: str):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None:
			return await ctx.send("Setup is not done yet or Error has happaned")
		await ctx.channel.send(f"Please avoid going off topic, {user}. You can have unrelated conversations in <#{data['general']}> or <#{data['eng_chat']}>")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="say", description="simple say command",guild_ids=guild_ids, default_permission=False, permissions=staff_perm,
		options=[create_option(name="str", description="Type Thing that bot need to send", option_type=3, required=True),
		create_option(name="reply", description="Enter Message id you want to reply", option_type=3, required=False),
		create_option(name="ping", description="you want to ping the user ?", option_type=5, required=False)]
		)
	@commands.cooldown(3,60 , commands.BucketType.user)
	async def say(self, ctx, str:str, reply: int=None, ping: bool=True):
		if reply:
			try:
				message = await ctx.channel.fetch_message(reply)
			except:
				return await ctx.send("make Sure your in the same chanenl as message or check your message id",hidden=True)

			await message.reply(f"{str}", mention_author=ping)
			await ctx.send(f"You Said: {str}\nTo {message.author.name}", hidden=True)
		if not reply:
			await ctx.channel.send(f"{str}",allowed_mentions=discord.AllowedMentions(users=True, everyone=False, roles=False, replied_user=False))
			await ctx.send(f"You Said: {str} in {ctx.channel.mention}", hidden=True)

	@cog_ext.cog_slash(name="pin", guild_ids=guild_ids, description="refer someone to channel pin message",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),
		]
	)
	async def pin(self, ctx, user: str):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None:
			return await ctx.send("Setup is not done yet or Error has happaned")
		await ctx.channel.send(f"Please refer to this channel's pinned messages for further information, {user}\n▪︎PC: Click on the pin icon located in the top-right of the channel.\n▪︎ Mobile: Click on the channel name and select Pins located at the top.")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="faq", guild_ids=guild_ids, description="refer someone to faq channel",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),
		]
	)
	async def faq(self, ctx, user: str):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None:
			return await ctx.send("Setup is not done yet or Error has happaned")
		await ctx.channel.send(f"Please refer to <#{data['faq']}> for further information, {user}. Make sure to read through the channel before asking questions in the support channels, as your questions could have been answered there.")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="lang", guild_ids=guild_ids, description="When someone uses language other than the allowed ones",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),
		]
	)
	async def lang(self, ctx, user: str):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None:
			return await ctx.send("Setup is not done yet or Error has happaned")
		await ctx.channel.send(f"Please do not use any other language aside from {data['lang']} in this channel. {user}")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="eng", guild_ids=guild_ids, description="When someone uses other than English in english chat",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),])
	async def eng(self, ctx, user: str):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None:
			return await ctx.send("Setup is not done yet or Error has happaned")
		await ctx.channel.send(f"Please do not use any other language aside from English in this channel. {user}")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="official", guild_ids=[814374218602512395], description="When someone ask if server is official",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),])
	async def official(self, ctx, user: str):
		await ctx.channel.send(f"{user} ,This is the Oldest and Biggest community of **PUBG : NEW STATE INDIA**.\n\nThere is no official server for **PUBG : NEW STATE**.")
		await ctx.send("done",hidden=True)

	@cog_ext.cog_slash(name="news", guild_ids=guild_ids, description="When someone ask for New State News",default_permission=False, permissions=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True),])
	async def news(self, ctx, user: str):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None:
			return await ctx.send("Setup is not done yet or Error has happaned")
		await ctx.channel.send(f"{user} , Keep your eyes on <#{data['new']}> or follow **PUBG : NEW STATE** official social media accounts for the latest news.")
		await ctx.send("done",hidden=True)
	
	@cog_ext.cog_slash(name="media". guild_ids=guild_ids, description="When someone send Image not relted to newstate in media"default_permisson=False, permissons=staff_perm,
		options=[create_option(name="user", description="Select users to reply", option_type=3,required=True)])
	async def media(self, ctx, user: str):
		await ctx.send("Done", hidden=True)
		if ctx.guild.id == 814374218602512395:
			await ctx.channel.send(f"Kindly do not post content in <#814383272456618054> unrelated to PUBG NEW {user}")
		if ctx.guild.id == 829615142450495601:
			await ctx.channel.send(f"Kindly do not post content in <#829615143124992021> unrelated to PUBG NEW {user}")

def setup(bot):
	bot.add_cog(Misc(bot))
