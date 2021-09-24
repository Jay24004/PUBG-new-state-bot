import discord
from discord.ext import commands

class auto(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		if message.content in ['?rank', '?top', '?profile']:
			if message.channel.id in [887252550347264021, 814383734387638272,882612020355162163, 882556009216884758]:
				return

			if not message.channel.id in [887252550347264021, 814383734387638272, 882612020355162163, 882556009216884758]:
				if message.guild.id == 814374218602512395:
					return await message.channel.send(f"{message.author.mention}, this command is disabled here, please use the <#814383734387638272> for this command")

				if message.guild.id == 829615142450495601:

					return await message.channel.send(f"{message.author.mention}, this command is disabled here, please use the <#882612020355162163> for this command")




def setup(bot):
	bot.add_cog(auto(bot))