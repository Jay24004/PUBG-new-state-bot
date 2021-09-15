import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

admin_perms = {
	829615142450495601: [
	create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	]
}

guild_ids = [829615142450495601]
class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} has been loaded")


	@cog_ext.cog_slash(name="itgnore_channel", description="add channel to ignore", guild_ids=guild_ids, default_permission=False,options=[
		create_option(name="Channel", description="Select channel", required=False, option_type=7)]
	)
	async def ignore(self, ctx, channel: discord.TextChannel):
		if channel != None:
			data = await self.bot.config.find(ctx.guild.id)
			try:
				if channel.id in data['ignore_channel']:
					data['ignore_channel'].remove(channel.id)
					return await ctx.send(f"The {channel.mention} is removed from the ignore list")

				data['ignore_channel'].append(channel.id)
			except KeyError:
				data['ignore_channel'] = []
				data['ignore_channel'].append(channel.id)

			await ctx.send(f"The {channel.mention} is now added to ignore channels list.", hidden=True)

		else:
			data = await self.bot.config.find(ctx.guild.id)
			try:
				channel_list = data['ignore_channel']
			except KeyError:
				return await ctx.send("There are no channel in the ignore list.")

			embed, i = discord.Embed(title="Ignore channels list", color=0x046402,description=""), 1
			for channel in channel_list:
				i += 1
				channel = self.bot.get_channel(channel)
				embed.description += f"{i}. {channel.mention}"

			await ctx.send(embed=embed, hidden=True)




def setup(bot):
	bot.add_cog(admin(bot))