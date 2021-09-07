import praw
import discord
from discord.ext import commands
import random
import asyncio
import datetime
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice




guild_ids=[829615142450495601]

reddit_api = praw.Reddit(client_id="TTD47ulffpWTZqxcM0zV1w",
						client_secret="NHPCoE4x90koXa_BnQgvA7u3gkmAmQ",
						username="nsdb-bot",
						password="jay24004",
						user_agent="hmm",
						check_for_async=False)

class reddit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} has been loaded")

	@cog_ext.cog_slash(name="reddit", description="Get some nice content from selected subreddits.",guild_ids=guild_ids,
		options=[
		create_option(name="reddit",
			required=True,
			description="Select reddit",
			option_type=3,
			choices=[
			create_choice(
				name="r/aww",
				value="aww"
				),
			create_choice(
				name="r/eyebleach",
				value="eyebleach"
				),
			create_choice(
				name="r/food",
				value="food"
				),
			create_choice(
				name="r/wholesomememes",
				value="wholesomememes"
				),
			create_choice(
				name="r/Awwducational",
				value="Awwducational/"
				),
			create_choice(
				name="r/CozyPlaces",
				value="CozyPlaces"
				),
			])
		])
	async def reddit(self, ctx, reddit: str):
		await ctx.defer()
		subreddit = reddit_api.subreddit(reddit)
		allsubs = []
		top = subreddit.top(limit = 50)
		for submission in top: 
			allsubs.append(submission)

		post = random.choice(allsubs)

		extension = post.url[len(post.url) - 3 :].lower()
		print(extension)
		while extension != "jpg" or "png":
			post = random.choice(allsubs)
			extension = post.url[len(post.url) - 3 :].lower()
			print(extension)
			if extension == "jpg" or "png": break

		embed = discord.Embed(description=f"**{post.title}**\nPosted By: {post.author}\nTotal upvotes: {post.score}\nPost Link: [here](https://www.reddit.com/{post.permalink})",color=ctx.author.colour)
		embed.set_image(url=post.url)
		embed.set_footer(text=f"Request by {ctx.author}",icon_url=ctx.author.avatar_url)
		embed.timestamp = datetime.datetime.utcnow()
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(reddit(bot))