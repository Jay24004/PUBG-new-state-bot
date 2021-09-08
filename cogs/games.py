import discord
from discord.ext import commands
import random
import asyncio 
import datetime
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext

guild_ids=[829615142450495601]

class games(commands.Cog):
	def __init__ (self, bot):
		self.bot = bot





	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} has been loaded")


	@cog_ext.cog_slash(name="Cointoss", description="Coin-toss game",guild_ids=guild_ids,
		options=[
				create_option(name="choices",
					description="Heads or Tails",
					required=True,
					option_type=3,
					choices=[
					create_choice(
							name='Head',
							value="head"
						),
					create_choice(
						name="Tail",
						value="tail"
						)
					]
				)
			]
	)
	@commands.cooldown(3,60 , commands.BucketType.user)
	async def cointoss(self, ctx, choices: str):
		side = random.choice(['head', 'tail','head','tail','head','head','tail','tail','tail','head', 'head'])
		print(side)
		if choices == side:
			embed = discord.Embed(title=f"{ctx.author} You won!",colour=0x2ECC71)
			embed.set_footer(text="my badluck", icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['cointoss']['win'] += 1
			await self.bot.score.upsert(data)
			await ctx.send(embed=embed)
		if side != choices:
			embed = discord.Embed(title=f"{ctx.author} You Lost!",colour=0xE74C3C)
			embed.set_footer(text="Try again later", icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['cointoss']['lost'] += 1
			await self.bot.score.upsert(data)
			await ctx.send(embed=embed)

	@cog_ext.cog_slash(name="RPS", description="Play Rock-Paper-Scissors",guild_ids=guild_ids,
		options=[
				create_option(name="choices",
					description="rock/paper/scissors",
					required=True,
					option_type=3,
					choices=[
					create_choice(
							name='Rock',
							value="rock"
						),
					create_choice(
						name="paper",
						value="paper"
						),
					create_choice(
						name="Scissors",
						value="scissors"
						)
					]
				)
			]
	)
	@commands.cooldown(3,60 , commands.BucketType.user)
	async def rps(self, ctx, choices: str):
		choices = choices.lower()
		side = ["rock","paper","scissors","rock","paper","scissors","rock","paper","scissors","rock","paper","scissors"]

		if choices not in ["rock","paper","scissors"]:
			return await ctx.send("Select An valid arguments", hidden=True)

		side = random.choice(side)
		if choices == "rock" and side == "paper":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {self.bot.user.mention}",colour=0xE74C3C)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['rps']['lost'] += 1
			await self.bot.score.upsert(data)
			return await ctx.send(embed=embed)
			return await ctx.send(embed=embed)

		if choices == "paper" and side == "rock":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {ctx.author.mention}",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['rps']['win'] += 1
			await self.bot.score.upsert(data)
			return await ctx.send(embed=embed)

		if choices == "scissors" and side =="rock":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {self.bot.user.mention}",colour=0xE74C3C)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['rps']['lost'] += 1
			await self.bot.score.upsert(data)
			return await ctx.send(embed=embed)

		if choices == "rock" and side == "scissors":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {ctx.author.mention}",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['rps']['win'] += 1
			await self.bot.score.upsert(data)
			return await ctx.send(embed=embed)			

		if choices == "paper" and side == "scissors":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {self.bot.user.mention}",colour=0xE74C3C)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['rps']['lost'] += 1
			return await ctx.send(embed=embed)			

		if choices == "scissors" and side == "paper":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {ctx.author.mention}",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			data = await self.bot.score.find(ctx.author.id)
			if data is None:
				data = {'_id': ctx.author.id,'rps': {'win': 0, 'lost': 0},'tic_tac':  {'win': 0, 'lost': 0, 'tie': 0},'cointoss':  {'win': 0, 'lost': 0}}
			data['rps']['win'] += 1
			await self.bot.score.upsert(data)
			return await ctx.send(embed=embed)

		if choices == side:
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: None",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			return await ctx.send(embed=embed)

	@cog_ext.cog_slash(name="Scores", description="Check Your Score",
		guild_ids=guild_ids, options=[
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


def setup(bot):
	bot.add_cog(games(bot))