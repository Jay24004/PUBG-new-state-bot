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


	@cog_ext.cog_slash(name="cointoss", description="Coin-toss game",guild_ids=guild_ids,
		options=[
				create_option(name="choices",
					description="Head / Tail",
					required=True,
					option_type=3,
					choices=[
					create_choice(
							name='head',
							value="head"
						),
					create_choice(
						name="tail",
						value="tail"
						)
					]
				)
			]
	)
	async def cointoss(self, ctx, choices: str):
		side = random.choice(['head', 'tail','head','tail','head','head','tail','tail','tail','head', 'head'])
		print(side)
		if choices == side:
			embed = discord.Embed(title=f"{ctx.author.mention} You won!",colour=0x2ECC71)
			embed.set_footer(text="my badluck", icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()

			await ctx.send(embed=embed)
		if side != choices:
			embed = discord.Embed(title=f"{ctx.author.mention} You Lost!",colour=0xE74C3C)
			embed.set_footer(text="Try again later", icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()

			await ctx.send(embed=embed)

	@cog_ext.cog_slash(name="spc", description="stone-paper-scissors ",guild_ids=guild_ids,
		options=[
				create_option(name="choices",
					description="stone/paper/scissors",
					required=True,
					option_type=3,
					choices=[
					create_choice(
							name='stone',
							value="stone"
						),
					create_choice(
						name="paper",
						value="paper"
						),
					create_choice(
						name="scissors",
						value="scissors"
						)
					]
				)
			]
	)
	async def spc(self, ctx, choices: str):
		side = ["stone","paper","scissors","stone","paper","scissors","stone","paper","scissors","stone","paper","scissors"]

		if choices not in ["stone","paper","scissors"]:
			return await ctx.send("Select An valid arguments", hidden=True)

		side = random.choice(side)
		print(side)
		if choices == "stone" and side == "paper":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {self.bot.user.mention}",colour=0xE74C3C)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)

		if choices == "paper" and side == "stone":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {ctx.author.mention}",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)

		if choices == "scissors" and side =="stone":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {self.bot.user.mention}",colour=0xE74C3C)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)

		if choices == "stone" and side == "scissors":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {ctx.author.mention}",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)			

		if choices == "paper" and side == "scissors":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {self.bot.user.mention}",colour=0xE74C3C)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)			

		if choices == "scissors" and side == "paper":
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: {ctx.author.mention}",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)

		if choices == side:
			embed = discord.Embed(description=f"{ctx.author.mention} choice: {choices}\n{self.bot.user.mention}: {side}\nWinner: None",colour=0x2ECC71)
			embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
			embed.timestamp = datetime.datetime.utcnow()
			return await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(games(bot))