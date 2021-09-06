import datetime
import discord
import re
import random
from typing import Union
from humanfriendly import format_timespan
from discord.ext import commands
import asyncio
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


admin_perms = {
	785839283847954433: [
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
	create_permission(803635405638991902, SlashCommandPermissionType.ROLE, True),
	create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
	create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
	]
}

mod_perms = {
	785839283847954433:[
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
	create_permission(803635405638991902, SlashCommandPermissionType.ROLE, True),
	create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
	create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
	create_permission(787259553225637889, SlashCommandPermissionType.ROLE, True),
	create_permission(843775369470672916, SlashCommandPermissionType.ROLE, True)
	]
}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)

description="Some slash commands form the modreation Cog but as slash"

guild_ids=[785839283847954433]
class slash(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} has been loaded \n------")

	@cog_ext.cog_slash(name="ban", description="Ban user From the Server", guild_ids=guild_ids,default_permission=False,
		permissions=mod_perms,
		options=[
				create_option(
					name="user",
					description="Select You that need to be ban",
					option_type=6,
					required=True
				),
				create_option(
					name="reason",
					description="Tell why you want to ban that user",
					option_type=3,
					required=True,
				),
				create_option(
					name="time",
					description="How much time they need to ban exp: 1h | 4d etc",
					option_type=3,
					required=False
				)
			]
		)
	async def ban(self , ctx: SlashContext, user: discord.Member, reason:str, time=None):
		time = time if time else None
		if user.top_role >= ctx.author.top_role:
			return await ctx.send("You cannot do this action on this user due to role hierarchy.")

		try:
			await user.send(f"You have been Banned from {ctx.guild.name} for {reason}")
		except discord.HTTPException:
			pass

		await ctx.guild.ban(user, reason=reason, delete_message_days=0)

		em = discord.Embed(color=0x06f79e, description=f"**{user.name}** Has been Banned for {reason}")
		await ctx.send(embed=em)

		log_channel = self.bot.get_channel(855784930494775296)
		data = await self.bot.config.find(ctx.guild.id)
		
		log_embed = discord.Embed(title=f"🔨 Ban | Case ID: {data['case']}",
		    description=f" **Offender**: {user} | {user.mention} \n**Reason**: {reason}\n **Moderator**: {ctx.author} {ctx.author.mention}", color=0xE74C3C)
		log_embed.set_thumbnail(url=user.avatar_url)
		log_embed.timestamp = datetime.datetime.utcnow()
		log_embed.set_footer(text=f"ID: {user.id}")

		await log_channel.send(embed=log_embed)
		data["case"] += 1
		
		return await self.bot.config.upsert(data)

		time = await TimeConverter().convert(ctx, time)
		data = {
		    '_id': user.id,
		    'BannedAt': datetime.datetime.now(),
		    'BanDuration': time or None,
		    'BanedBy': ctx.author.id,
		    'guildId': ctx.guild.id,
		}
		if time is None:
			pass
		else:
			await self.bot.bans.upsert(data)
			self.bot.ban_users[user.id] = data
			time = format_timespan(time)

	@cog_ext.cog_slash(name="force_ban", description="Ban user only works with Ids", guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(
					name="user",
					description="Select You that need to be ban",
					option_type=3,
					required=True
				),
				create_option(
					name="reason",
					description="Tell why you want to ban that user",
					option_type=3,
					required=True,
				),
				create_option(
					name="time",
					description="How much time they need to ban exp: 1h | 4d etc",
					option_type=3,
					required=False
				)
			]
		)
	async def force_ban(self , ctx: SlashContext, user: int, reason:str, time=None):
		time = time if time else None
		user = await self.bot.fetch_user(user)
		try:
			await user.send(f"You have been Banned from {ctx.guild.name} for {reason}")
		except discord.HTTPException:
			pass

		await ctx.guild.ban(user, reason=reason, delete_message_days=0)

		em = discord.Embed(color=0x06f79e, description=f"**{user.name}** Has been Banned for {reason}")
		await ctx.send(embed=em)

		log_channel = self.bot.get_channel(855784930494775296)
		data = await self.bot.config.find(ctx.guild.id)
		log_embed = discord.Embed(title=f"🔨 Ban | Case ID: {data['case']}",
		    description=f" **Offender**: {user} | {user.mention} \n**Reason**: {reason}\n **Moderator**: {ctx.author} {ctx.author.mention}", color=0xE74C3C)
		log_embed.set_thumbnail(url=user.avatar_url)
		log_embed.timestamp = datetime.datetime.utcnow()
		log_embed.set_footer(text=f"ID: {user.id}")

		await log_channel.send(embed=log_embed)
		data["case"] += 1
		
		return await self.bot.config.upsert(data)

	time = await TimeConverter().convert(ctx, time)
	data = {
	    '_id': user.id,
	    'BannedAt': datetime.datetime.now(),
	    'BanDuration': time or None,
	    'BanedBy': ctx.author.id,
	    'guildId': ctx.guild.id,
	}
	if time is None:
		pass
	else:
		await self.bot.bans.upsert(data)
		self.bot.ban_users[user.id] = data
		time = format_timespan(time)
		
	@cog_ext.cog_slash(name="kick", description="Kick someone from the guild",default_permission=False,permissions=mod_perms,
		guild_ids=guild_ids,
		options=[
				create_option(
						name="user",
						description="Select which user need to kicked",
						option_type=6,
						required=True,
					),
				create_option(
					name="reason",
					description="Why your kicking that user",
					option_type=3,
					required=True,
					)
			]
		)
	async def kick(self, ctx: SlashContext, user, reason):
		if user.top_role >= ctx.author.top_role: return await ctx.send("You can't You cannot do this action on this user due to role hierarchy.")

		try:
			await user.send(f"You Have Been kicked from {ctx.guild} for {reason}")
		except:
			pass

		await ctx.guild.kick(user=user, reason=reason)
		emb = discord.Embed(color=0x06f79e, description=f"**{user.name}** Has Been kicked for {reason}")

		await ctx.send(embed=emb)

		log_channel = self.bot.get_channel(855784930494775296)
		data = await self.bot.config.find(ctx.guild.id)
		log_embed = discord.Embed(title=f"👢 Kick | Case ID: {data['case']}",
		    description=f" **Offender**: {user} | {user.mention}\n **Moderator**: {ctx.author.display_name} | {ctx.author.mention}\n **Reason**: {reason}.", color=0xE74C3C)
		log_embed.set_thumbnail(url=user.avatar_url)
		log_embed.timestamp = datetime.datetime.utcnow()
		await log_channel.send(embed=log_embed)

		data["case"] += 1
		await self.bot.config.upsert(data)
		
	@cog_ext.cog_slash(name="mute", description="Mute someone for x time", guild_ids=guild_ids,default_permission=False,permissions=mod_perms,
		options=[
			create_option(name="user", description="Select which User You want to Mute" , option_type=6, required=True),
			create_option(name="reason", description="Enter reason for the mute" , option_type=3, required=False),
			create_option(name="time", description="The time you want to mute user", option_type=3, required=False)
		]
	)
	async def mute(self, ctx: SlashContext, user, reason=None, time=None):
		reason = reason if reason else "N/A"
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if not role:
		    await ctx.send("No muted role was found! Please create one called `Muted`")
		    return

		try:
			if self.bot.muted_users[user.id]:
				await ctx.send("This user is already muted")
			return
		except KeyError:
			pass

		await user.add_roles(role)
		try:
			await user.send(f"You Have Been muted in {ctx.guild}\nTime: N/A, Reason: {reason}")
		except:
			pass

		em = discord.Embed(color=0x06f79e, description=f"**{user.name}** Has been Muted for {reason}")
		await ctx.send(embed=em)

		data = await self.bot.config.find(ctx.guild.id)
		log_channel = self.bot.get_channel(855784930494775296)

		log_embed = discord.Embed(title=f"🔇 Mute | Case ID: {data['case']}",
			description=f" **Offender**: {user} | {user.mention}\n **Reason**: {reason}\n **Duration**: None \n **Moderator**: {ctx.author.display_name} | {ctx.author.mention}",
			color=0x706e6d)
		log_embed.set_thumbnail(url=user.avatar_url)
		log_embed.timestamp = datetime.datetime.utcnow()
		log_embed.set_footer(text=f"ID: {user.id}")

		await log_channel.send(embed=log_embed)

		data["case"] += 1
		return await self.bot.config.upsert(data)

		time = await TimeConverter().convert(ctx, time)

		data = {
			'_id': user.id,
			'mutedAt': datetime.datetime.now(),
			'muteDuration': time or None,
			'mutedBy': ctx.author.id,
			'guildId': ctx.guild.id,
		}
		if time is None:
			pass
		else:
			await self.bot.mutes.upsert(data)
			self.bot.muted_users[user.id] = data

	@cog_ext.cog_slash(name="Unmute", description="Unmute an User", guild_ids=guild_ids,default_permission=False, permissions=mod_perms,
		options=[
				create_option(name="user", description="Select which User need be Unmuted", option_type=6, required=True),
				create_option(name="reason", description="reason why your unmuting user early", option_type=3, required=False)
			]
		)
	async def unmute(self, ctx:SlashContext, user, reason):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if not role:
		    await ctx.send("No muted role was found! Please create one called `Muted`")
		    return
		reason = reason if reason else "N/A"
		await self.bot.mutes.delete(user.id)
		try:
			self.bot.muted_users.pop(user.id)
		except KeyError:
			pass

		if role not in user.roles:
			await ctx.send("This user is not muted.")
			return

		await user.remove_roles(role)
		embed = discord.Embed(description=f"{user} Has been Unmuted",color=0x2ECC71)
		await ctx.send(embed=embed)

		log_channel = self.bot.get_channel(855784930494775296)
		data = await self.bot.config.find(ctx.guild.id)
		log_embed = discord.Embed(title=f"🔊 UnMute | Case ID: {data['case']}",
			description=f" **Offender**: {user.name} | {user.mention} \n**Reason**: {reason}\n**Moderator**: {ctx.author.display_name} {ctx.author.mention}", color=0x2ECC71)
		log_embed.set_thumbnail(url=user.avatar_url)
		log_embed.timestamp = datetime.datetime.utcnow()
		log_embed.set_footer(text=f"ID: {user.id}")

		await log_channel.send(embed=log_embed)

		data["case"] += 1
		await self.bot.config.upsert(data)

def setup(bot):
	bot.add_cog(slash(bot))
