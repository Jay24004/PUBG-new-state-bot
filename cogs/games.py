import discord
from discord.ext import commands
import random
import asyncio 
import datetime
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_button, ButtonStyle
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext

class games(commands.Cog):
	def __init__ (self, bot):
		self.bot = bot

	def is_bot_channel():
		async def predicate(ctx):
			data = await ctx.bot.config.find(ctx.guild.id)
			if data is None: return await ctx.send("This is not a bot-channel or there is no bot channel in server", hidden=True)
			if data:
				return ctx.channel.id == data['bot_channel'] or ctx.channel.id in data['bot-channel']
		return commands.check(predicate)

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@cog_ext.cog_slash(name="cointoss", description="Coin-toss game",guild_ids=None)
	@is_bot_channel()
	@commands.cooldown(3,60 , commands.BucketType.user)
	async def cointoss(self, ctx):
		main_embed = discord.Embed(title=f"{ctx.author.name}'s cointoss",description="Select your Side Head or Tail, You have 30s to select one", color=0x2f3136)
		main_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
		main_embed.timestamp = datetime.datetime.now()

		buttons = [create_button(style=ButtonStyle.green,label="Heads", emoji=None),create_button(style=ButtonStyle.blurple,label="Tails", emoji=None), create_button(style=ButtonStyle.red,label="Exit", emoji=None,)]
		msg = await ctx.send(embed=main_embed, components=[create_actionrow(*buttons)])
		choices = random.choice(["heads", "tails"])


		while True:
			def custom_check(component_ctx: ComponentContext) -> bool:
				if component_ctx.author == ctx.author:
					return True
			try:
				res: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(*buttons)], check=custom_check, timeout=30)
				await res.defer(hidden=True, ignore=True)
				player_choice = res.component['label'].lower()

				if player_choice == choices:
					winner_embed = discord.Embed(title=f"{ctx.author.name}'s cointoss", description = "You won the cointoss", color=0x2f3136)
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					winner_embed.timestamp = datetime.datetime.now()
					winner_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					data = await self.bot.score.find(ctx.author.id)
					await msg.edit(embed=winner_embed, components=[create_actionrow(*buttons)])

				if player_choice != choices:
					lost_embed = discord.Embed(title=f"{ctx.author.name}'s cointoss", description = "You Lost the cointoss", color=0x2f3136)
					lost_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					lost_embed.timestamp = datetime.datetime.now()
					await msg.edit(embed=lost_embed, components=[create_actionrow(*buttons)])

				if res.component['label'].lower() == "again":
					buttons = [create_button(style=ButtonStyle.green,label="Heads", emoji=None),create_button(style=ButtonStyle.blurple,label="Tails", emoji=None), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=main_embed, components=[create_actionrow(*buttons)])

				if res.component['label'].lower() == "exit":
					await msg.edit(components=[])
					
			except asyncio.TimeoutError:
				await msg.edit(components=[])

	@cog_ext.cog_slash(name="RPS", description="Play Rock-Paper-Scissors",guild_ids=None)
	@is_bot_channel()
	@commands.cooldown(3,60 , commands.BucketType.user)
	async def rps(self, ctx):

		main_embed = discord.Embed(title=f"{ctx.author.name}'s RPS", description="Select your tool from below buttons, you have 30s to select",colour=0x2f3136)
		main_embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
		main_embed.timestamp = datetime.datetime.now()

		buttons = [create_button(style=ButtonStyle.grey, label="Rock", emoji="🤜"), create_button(style=ButtonStyle.green, label="paper", emoji="✋"), create_button(style=ButtonStyle.blurple, label="scissors", emoji="✌️")]
		msg = await ctx.send(embed=main_embed, components=[create_actionrow(*buttons)])

		
		while True:
			def custom_check(component_ctx: ComponentContext) -> bool:
				if component_ctx.author == ctx.author:
					return True
			try:
				
				res: ComponentContext= await wait_for_component(self.bot, components=[*buttons], check=custom_check, timeout=30)
				await res.defer(ignore=True)
				user = res.component['label'].lower()
				ai = random.choice(["rock","paper","scissors"])

				if user == "rock" and ai == "paper":
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value="🤜", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value="✋", inline=True)
					embed.add_field(name="Result", value="You Lost!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if user == "paper" and ai == "rock":
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value="✋", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value="🤜", inline=True)
					embed.add_field(name="Result", value="You won!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()

					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if user == "scissors" and ai =="rock":
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value="✌️", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value="🤜", inline=True)
					embed.add_field(name="Result", value="You Lost!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if user == "rock" and ai == "scissors":
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value="🤜", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value="✌️", inline=True)
					embed.add_field(name="Result", value="You Won!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if user == "paper" and ai == "scissors":
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value="✋", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value="✌️", inline=True)
					embed.add_field(name="Result", value="You Lost!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if user == "scissors" and ai == "paper":
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value="✌️", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value="✋", inline=True)
					embed.add_field(name="Result", value="You Won!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if user == ai:
					embed = discord.Embed(title=f"{ctx.author.name}'s RPS",colour=0x2f3136)
					embed.add_field(name=ctx.author.name, value=f"{res.component['emoji']['name']}", inline=True)
					embed.add_field(name="VS", value="⚡", inline=True)
					embed.add_field(name=self.bot.user.name, value=f"{res.component['emoji']['name']}", inline=True)
					embed.add_field(name="Result", value="It's Draw!", inline=False)
					embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
					embed.timestamp = datetime.datetime.utcnow()
					buttons = [create_button(style=ButtonStyle.green,label="Again", emoji="🔁"), create_button(style=ButtonStyle.red,label="Exit", emoji="❎")]
					await msg.edit(embed=embed, components=[create_actionrow(*buttons)])

				if res.component['label'].lower() == "again":
					buttons = [create_button(style=ButtonStyle.grey, label="Rock", emoji="🤜"), create_button(style=ButtonStyle.green, label="paper", emoji="✋"), create_button(style=ButtonStyle.blurple, label="scissors", emoji="✌️")]
					await msg.edit(embed=main_embed,components=[create_actionrow(*buttons)])

				if res.component['label'].lower() == "exit":
					await msg.edit(components=[])
			except asyncio.TimeoutError:
				await msg.edit(components=[])
	"""
	@cog_ext.cog_slash(name="Scores", description="Check Your Score",
		guild_ids=None, options=[
				create_option(name="game", description="Select game",required=True, option_type=3,choices=[
					create_choice(name="Cointoss",value='coin'),
					create_choice(name="RPS", value="rps"),
					create_choice(name="TicTacToe", value="tic_tac")
					]
				),
				create_option(name="user", description="Select user", required=False, option_type=6)
			]
		)
	@commands.cooldown(3,60 , commands.BucketType.user)
	async def score(self, ctx, game: str, user: discord.Member=None):
		user = user if user else ctx.author
		data = await self.bot.score.find(user.id)
		if data is None:
			if user == ctx.author:
				return await ctx.send("You haven't played the game yet.")
			if user != ctx.author:
				return await ctx.send(f"{user.name} hasn't played the game yet.")

		if game == 'coin':
			embed = discord.Embed(title=f"{user.name} Cointoss stats",colour=user.colour,
				description=f"**Win**: {data['cointoss']['win']}\n**Lose**: {data['cointoss']['lost']}")
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=embed, hidden=False)
		if game == 'rps':
			embed = discord.Embed(title=f"{user.name} RPS stats",colour=user.colour,
				description=f"**Win**: {data['rps']['win']}\n**Lose**: {data['rps']['lost']}")
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=embed, hidden=False)
		if game == 'tic_tac':
			embed = discord.Embed(title=f"{user.name} TicTacToe stats",colour=user.colour,
				description=f"**Win**: {data['tic_tac']['win']}\n**Tie**: {data['tic_tac']['tie']}\n**Lose**: {data['tic_tac']['lost']}")
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=embed, hidden=False)
	"""
def setup(bot):
	bot.add_cog(games(bot))