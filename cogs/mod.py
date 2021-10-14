import discord
from discord.ext import commands
import datetime
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
guild_ids = [814374218602512395, 829615142450495601,885802388001288262]

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

	def is_server_staff():
		async def predicate(ctx):
			if ctx.author == ctx.guild.owner: return True
			data = await ctx.bot.config.find(ctx.guild.id)
			if data:
				for roles in data['staff_role']:
					role = discord.utils.get(ctx.guild.roles, id=roles)
					return role in ctx.author.roles
		return commands.check(predicate)


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

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

	@cog_ext.cog_slash(name="whois", description="show usefull info about user", options=[
		create_option(name="user", description="select user", required=False, option_type=6)])
	@is_server_staff()
	async def whois(self, ctx , user: discord.Member=None):
		def fomat_time(time):
			return time.strftime('%d-%B-%Y %I:%m %p')

		member = user if user else ctx.author
		usercolor = member.color

		today = (datetime.datetime.utcnow() -
		member.created_at).total_seconds()

		embed = discord.Embed(title=f'{member.name}', color=usercolor)
		embed.set_thumbnail(url=member.avatar_url)
		embed.add_field(name='Account Name:',
			value=f'{member.name}', inline=False)
		embed.add_field(
			name='Created at:', value=f"{fomat_time(member.created_at)}\n{format_timespan(today)}")
		embed.add_field(name='Joined at', value=fomat_time(member.joined_at))
		embed.add_field(name='Account Status',
			value=str(member.status).title())
		embed.add_field(name='Account Activity',
			value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None")

		hsorted_roles = sorted(
		[role for role in member.roles[-2:]], key=lambda x: x.position, reverse=True)

		embed.add_field(name='Top Role:', value=', '.join(
			role.mention for role in hsorted_roles), inline=False)
		embed.add_field(name='Number of Roles',
			value=f"{len(member.roles) -1 }")
		embed.set_footer(text=f'ID {member.id}', icon_url=member.avatar_url)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Config(bot))