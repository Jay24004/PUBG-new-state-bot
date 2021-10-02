import datetime
import asyncio 
import re
import random
import discord
from discord.ext import commands, tasks
from copy import deepcopy
import datetime
from dateutil.relativedelta import relativedelta
from humanfriendly import format_timespan
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from amari import AmariClient

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")

time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}
guild_ids=[814374218602512395, 885802388001288262, 829615142450495601, 888085276801531967]

admin_perms = {
	814374218602512395:[
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
	create_permission(886551491744264222, SlashCommandPermissionType.ROLE, True)
	],
	829615142450495601: [	#BD
	create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(829615142450495609, SlashCommandPermissionType.ROLE, True),
	create_permission(829615142450495608, SlashCommandPermissionType.ROLE, True)
	],
	885802388001288262:[	#FRANCE
	create_permission(885814181549457418, SlashCommandPermissionType.ROLE, True),
	create_permission(885815298110918666, SlashCommandPermissionType.ROLE, True),
	create_permission(888409306616168560, SlashCommandPermissionType.ROLE, True),
	create_permission(890486198471098368, SlashCommandPermissionType.ROLE, True),
	create_permission(885814690138189824, SlashCommandPermissionType.ROLE, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True)
	],
	888085276801531967: [
	create_permission(888085276801531967, SlashCommandPermissionType.ROLE, True),
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

class giveaway(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.giveaway_task = self.check_givaway.start()
		
	def cog_unload(self):
		self.giveaway_task.cancel()
	
	@tasks.loop(seconds=10)
	async def check_givaway(self):
		currentTime = datetime.datetime.now()
		giveaway = deepcopy(self.bot.giveaway)
		for key, value in giveaway.items():
			ftime = value['start_time'] + relativedelta(seconds=value['end_time'])

			if currentTime >= ftime:
				guild = self.bot.get_guild(value['guild'])
				channel = guild.get_channel(value['channel'])
				try:
					message = await channel.fetch_message(key)
				except:
					await self.bot.give.delete(key)
					try:
						self.bot.giveaway.pop(key)
					except KeyError:
						pass
					return

				data = await self.bot.give.find(message.id)
				host = guild.get_member(value['host'])
				backup = {'_id': message.id, 'entries': [], 'channel': message.channel.id, 'time': datetime.datetime.now()}
				for user in data['entries']:
					backup['entries'].append(user)

				winner_list = []

				if len(data['entries']) < value['winners']:
					embeds = message.embeds
					for embed in embeds:
						edict = embed.to_dict()

					edict['title'] = f"{edict['title']} • Giveaway Has Ended"
					edict['color'] = 15158332
					edict['description'] = re.sub(r'(Ends)',r'Ended', edict['description'])
					
					emojig = self.bot.get_guild(888085276801531967)
					emoji = await emojig.fetch_emoji(893744091710509097)
					emoji2 = await emojig.fetch_emoji(893787497920876544)
					buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", emoji=emoji, disabled=True)]
					await message.edit(embed=embed.from_dict(edict), components=[create_actionrow(*buttons)])

					small_embed = discord.Embed(description=f"No valid [entrants]({message.jump_url}) so the winner could not be determined", color=0x2f3136)
					await message.reply(embed=small_embed)
					await self.bot.give.delete(message.id)
					try:
						self.bot.giveaway.pop((data['_id']))
					except KeyError:
						pass
					return 

				entries = len(data['entries'])
				while True:
					member = random.choice(data['entries'])
					data['entries'].remove(member)
					member = guild.get_member(member)
					winner_list.append(member.mention)
					if len(winner_list) == value['winners']: break

				if len(winner_list) >= value['winners']:
					embeds = message.embeds
					for embed in embeds:
						gdata = embed.to_dict()
					winners = ",".join(winner_list)
					small_embed = discord.Embed(description=f"Total Entries: [{entries}]({message.jump_url})")
					await message.reply(
					f"Congratulations {winners}! You won the {gdata['title']}",embed=small_embed)

					gdata['title'] = f"{gdata['title']} • Giveaway Has Ended"
					gdata['description'] = re.sub(r'(Ends)',r'Ended', gdata['description'])
					gdata['color'] = 15158332
					field = {'name': "Winner!", 'value': ", ".join(winner_list), 'inline': False}
					try:
						gdata['fields'].append(field)
					except KeyError:
						gdata['fields'] = []
						gdata['fields'].append(field)

					emojig = self.bot.get_guild(888085276801531967)
					emoji = await emojig.fetch_emoji(893744091710509097)
					emoji2 = await emojig.fetch_emoji(893787497920876544)
					buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {entries}", emoji=emoji, disabled=True)]

					await message.edit(embed=embed.from_dict(gdata), components=[create_actionrow(*buttons)])
					await self.bot.give.delete(message.id)

					try:
						self.bot.giveaway.pop(message.id)
					except KeyError:
						pass

					print(backup)
					await self.bot.endgive.upsert(backup)
					await self.bot.give.delete(data)

	@check_givaway.before_loop
	async def before_check_givaway(self):
		await self.bot.wait_until_ready()
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):
		if ctx.custom_id == "Giveaway:Enter":
			#await ctx.defer(hidden=True)
			data = await self.bot.give.find(ctx.origin_message.id)
			amari_api = AmariClient(self.bot.amari)
			message = await ctx.channel.fetch_message(ctx.origin_message.id)
			guild, user = ctx.guild, ctx.author
			if ctx.author.bot: return

			if data['r_req']:
				required_role = discord.utils.get(guild.roles, id=data['r_req'])
				if required_role in user.roles:
					pass
				else:
					if data['b_role']:
						bypass_role = discord.utils.get(guild.roles, id=data['b_role'])
						if bypass_role in user.roles:
							pass
						else:
							embed = discord.Embed(title="Entry Declined:",
								description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{required_role.name}`",color=0xE74C3C)
							embed.timestamp = datetime.datetime.utcnow()
							embed.set_footer(text=guild.name,icon_url=guild.icon_url)
							try:
								await user.send(embed=embed)
							except discord.HTTPException:
								pass
							return await ctx.send("Your Entery has been declined because you don't meet the requirment", hidden=True)
					else:
						embed = discord.Embed(title="Entry Declined:",
								description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{required_role.name}`",color=0xE74C3C)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
						try:
							await user.send(embed=embed)
						except discord.HTTPException:
							pass
						return await ctx.send("Your Entery has been declined because you don't meet the requirment", hidden=True)

			if data['amari_level']:
				user_level = await amari_api.fetch_user(user.guild.id, user.id)
				if user_level.level < data['amari_level']:
					if data['b_role']:
						role = discord.utils.get(guild.roles, id=data['b_role'])
						if role in user.roles:
							pass
						else:
							embed = discord.Embed(title="Entery Decline:",
								description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:You don't have Required amari level to join the giveaway `{required['amari_level']}`", color=0xE74C3C)
							embed.timestamp = datetime.datetime.utcnow()
							embed.set_footer(text=guild.name,icon_url=guild.icon_url)
							try:
								await user.send(embed=embed)
							except discord.HTTPException:
								pass
							return await ctx.send("Your Entery has been declined because you don't meet the requirment", hidden=True)
					else:
						embed = discord.Embed(title="Entery Decline:",
							description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:Required amari level to join the giveaway `{required['amari_level']}`", color=0xE74C3C)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
						try:
							await user.send(embed=embed)
						except discord.HTTPException:
							pass 
						return await ctx.send("Your Entery has been declined because you don't meet the requirment", hidden=True)

			if data['weekly_amari']:
				user_level = await amari_api.fetch_user(user.guild.id, user.id)
				if user_level.weeklyexp < data['weekly_amari']:
					if data['b_role']:
						role = discord.utils.get(guild.roles, id=data['b_role'])
						if role in user.roles:
							pass
						else:
							embed = discord.Embed(title="Entery Decline:",
								description=f"Your Entry to this [Giveaway]({message.jump_url}).has been denied.\nReason:You don't have the required Weekly Amari points `{required['weekly_amari']}`", color=0xE74C3C)
							embed.timestamp = datetime.datetime.utcnow()
							embed.set_footer(text=guild.name,icon_url=guild.icon_url)
							try:
								await user.send(embed=embed)
							except discord.HTTPException:
								pass 
							return await ctx.send("Your Entery has been declined because you don't meet the requirment", hidden=True)
					else:
						embed = discord.Embed(title="Entery Decline:",
							description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:You don't have Required Weekly Amari `{required['weekly_amari']}`", color=0xE74C3C)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
						try:
							await user.send(embed=embed)
						except discord.HTTPException:
							pass
						return await ctx.send("Your Entery has been declined because you don't meet the requirment", hidden=True)

			if ctx.author.id in data['entries']:
				data['entries'].remove(ctx.author.id)
				await self.bot.give.upsert(data)
				self.bot.giveaway[message.id] = data
				emojig = self.bot.get_guild(888085276801531967)
				emoji = await emojig.fetch_emoji(893744091710509097)
				emoji2 = await emojig.fetch_emoji(893787497920876544)
				buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", emoji=emoji, disabled=True)]
				await message.edit(components=[create_actionrow(*buttons)])
				return await ctx.send("You Successfully Removed your Entery from this giveaway", hidden=True)

			if ctx.author.id not in data['entries']:
				data['entries'].append(ctx.author.id)
				await self.bot.give.upsert(data)

				self.bot.giveaway[message.id] = data
				emojig = self.bot.get_guild(888085276801531967)
				emoji = await emojig.fetch_emoji(893744091710509097)
				emoji2 = await emojig.fetch_emoji(893787497920876544)
				buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", emoji=emoji, disabled=True)]

				await message.edit(components=[create_actionrow(*buttons)])
				return await ctx.send("you have successfully Entered Giveaway", hidden=True)

	@cog_ext.cog_slash(name="gstart",description="A giveaway command", guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(name="time", description="How long the giveaway should last? i.e. 15s , 30m/h/d", option_type=3, required=True),
				create_option(name="price", description="price of the giveaway", option_type=3, required=True),
				create_option(name="winners", description="Number of the winners.", option_type=4, required=True),
				create_option(name="required_role", description="Required role to join the giveaway",option_type=8, required=False),
				create_option(name="bypass_role", description="bypass role to bypass the required role",option_type=8, required=False),
				create_option(name="amari_level", description="set required amari level",option_type=4, required=False),
				create_option(name="weekly_amari", description="set giveaway weekly amari",option_type=4, required=False),
				create_option(name="host", description="Is give is hosted by member give them credit", required=False, option_type=6),
				create_option(name="ping", description="Ping a role", option_type=8, required=False)
			]
		)
	async def gstart(self, ctx, time, price, winners,required_role=None, bypass_role=None, amari_level: int=None, weekly_amari: int=None,  host: discord.Member=None,ping:discord.Role=None):
		time = await TimeConverter().convert(ctx, time)
		if time < 15:
			return await ctx.send("Giveaway time needs to be longer than 15 seconds", hidden=True)
		end_time = datetime.datetime.now() + datetime.timedelta(seconds=time)

		end_time = round(end_time.timestamp())
		required_role = required_role if required_role else None
		bypass_role = bypass_role if bypass_role else None
		amari_level = amari_level if amari_level else None
		weekly_amari = weekly_amari if weekly_amari else None
		host = host if host else ctx.author

		embed_dict = {'type': 'rich', 'title': price, 'color': 1174692,
		'description': f"React to this message to Enter!!\nEnds: <t:{end_time}:R> (<t:{end_time}:F>)\nWinner: {winners}\nHosted By: {host.mention}",
		'fields': [],}
		if required_role == None:
			feild = {'name': "Role Requirements", 'inline':False}
			if bypass_role == None:
				pass
			else:
				feild['value'] = f"Bypass Role: {bypass_role.mention}"
				embed_dict['fields'].append(feild)
		else:
			feild = {'name': "Role Requirements:", 'inline':False}
			if bypass_role == None:
				feild['value'] = f"Required Role: {required_role.mention}"
				embed_dict['fields'].append(feild)
			else:
				feild['value'] = f"Required Role: {required_role.mention}\nBypass Role: {bypass_role.mention}"
				embed_dict['fields'].append(feild)

		feild = {'name': "Amari Requirements", 'inline': False}
		if amari_level != None and weekly_amari == None:
			feild['value'] = f"Required Amari Level: {amari_level}"
		if amari_level == None and weekly_amari != None:
			feild['value'] = f"Weekly Amari: {weekly_amari}"

		if amari_level != None and weekly_amari != None:
			feild['value'] = f"Amari Level: {amari_level}\nWeekly Amari: {weekly_amari}"
		if amari_level == None and weekly_amari == None:
			pass
		else:
			embed_dict['fields'].append(feild)

		embed = discord.Embed()
		eguild = self.bot.get_guild(888085276801531967)
		emoji2 = await eguild.fetch_emoji(893787497920876544)
		buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.grey, label="Total Entries: 0", disabled=True)]
		msg = await ctx.send(embed=embed.from_dict(embed_dict), components=[create_actionrow(*buttons)])
		data = {"_id": msg.id,
				"guild": ctx.guild.id,
				"channel": ctx.channel.id,
				"host": host.id,
				"winners": winners,
				"entries": [],
				"end_time": time,
				"start_time": datetime.datetime.now(),
				"weekly_amari": weekly_amari,
				"amari_level": amari_level
				}
		try:
			data['r_req'] = required_role.id
		except:
			data['r_req'] = None

		try:
			data['b_role'] = bypass_role.id
		except:
			data['b_role'] = None

		if ping == None:
			pass
		else:
			await ctx.channel.send(ping.mention,)

		await self.bot.give.upsert(data)
		self.bot.giveaway[msg.id] = data


	@cog_ext.cog_slash(name="gend", description="Force end a giveaway", guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(name="message_id", description="message id of the giveaway", required=True, option_type=3),
				create_option(name="channel", description="channel of the giveaway", required=True, option_type=7)
			]
		)
	async def gend(self, ctx, message_id, channel: discord.TextChannel=None):
		guild = ctx.guild
		message = await channel.fetch_message(int(message_id))
		data = await self.bot.give.find(message.id)
		if data is None: return await ctx.send("I can't Find anything in the Database check your message ID or its to old", hidden=True)
		
		data = await self.bot.give.find(message.id)
		host = guild.get_member(data['host'])
		backup = {'_id': message.id, 'entries': [], 'channel': message.channel.id, 'time': datetime.datetime.now()}
		for user in data['entries']:
			backup['entries'].append(user)

		winner_list = []

		if len(data['entries']) < data['winners']:
			embeds = message.embeds
			for embed in embeds:
				edict = embed.to_dict()

			edict['title'] = f"{edict['title']} • Giveaway Has Ended"
			edict['color'] = 15158332
			edict['description'] = re.sub(r'(Ends)',r'Ended', edict['description'])
			
			emojig = self.bot.get_guild(888085276801531967)
			emoji = await emojig.fetch_emoji(893744091710509097)
			emoji2 = await emojig.fetch_emoji(893787497920876544)
			buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", emoji=emoji, disabled=True)]
			await message.edit(embed=embed.from_dict(edict), components=[create_actionrow(*buttons)])

			small_embed = discord.Embed(description=f"No valid [entrants]({message.jump_url}) so the winner could not be determined", color=0x2f3136)
			await message.reply(embed=small_embed)
			await ctx.send("Giveaway has been ended", hidden=True)
			await self.bot.give.delete(message.id)
			try:
				self.bot.giveaway.pop((data['_id']))
			except KeyError:
				pass
			return 

		entries = len(data['entries'])
		while True:
			member = random.choice(data['entries'])
			data['entries'].remove(member)
			member = guild.get_member(member)
			winner_list.append(member.mention)
			if len(winner_list) == data['winners']: break

		if len(winner_list) >= data['winners']:
			embeds = message.embeds
			for embed in embeds:
				gdata = embed.to_dict()
			winners = ",".join(winner_list)
			small_embed = discord.Embed(description=f"Total Entries: [{entries}]({message.jump_url})")
			await message.reply(
			f"Congratulations {winners}! You won the {gdata['title']}",embed=small_embed)

			gdata['title'] = f"{gdata['title']} • Giveaway Has Ended"
			gdata['description'] = re.sub(r'(Ends)',r'Ended', gdata['description'])
			gdata['color'] = 15158332
			field = {'name': "Winner!", 'value': ", ".join(winner_list), 'inline': False}
			try:
				gdata['fields'].append(field)
			except KeyError:
				gdata['fields'] = []
				gdata['fields'].append(field)

			emojig = self.bot.get_guild(888085276801531967)
			emoji = await guild.fetch_emoji(893744091710509097)
			emoji2 = await guild.fetch_emoji(893787497920876544)
			buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {entries}", emoji=emoji, disabled=True)]

			await message.edit(embed=embed.from_dict(gdata), components=[create_actionrow(*buttons)])
			await ctx.send("Giveaway has been ended", hidden=True)
			await self.bot.give.delete(message.id)

			try:
				self.bot.giveaway.pop(message.id)
			except KeyError:
				pass

			print(backup)
			await self.bot.endgive.upsert(backup)
			await self.bot.give.delete(data)

	@cog_ext.cog_slash(name="greroll", description="Reroll the giveaway for new winners",guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
			create_option(name="channel", description="channel of giveaway message", required=True, option_type=7),
			create_option(name="message_id", description="message id of the giveaway", required=True, option_type=3),
			create_option(name="winners", description="numbers of winners", required=True, option_type=4),
			]
		)
	async def greroll(self, ctx, message_id, winners: int, channel=None,):
		try:
			message = await channel.fetch_message(int(message_id))
		except:
			return await ctx.send("Please ckeck your message id.", hidden=True)

		data = await self.bot.endgive.find(message.id)
		if not data:
			return await ctx.send("The Giveaway id not found or it's more than week old", hidden=True)

		winner_list = []
		users = data['entries']
		guild = ctx.guild
		while True:
			member = random.choice(users)
			users.remove(member)
			member = guild.get_member(member)
			winner_list.append(member.mention)
			if len(winner_list) == winners:break

		reply = ",".join(winner_list)
		embeds = message.embeds
		for embed in embeds:
			gdata = embed.to_dict()

		gdata['fields'] = []
		gdata['color'] = 15158332
		field = {'name': "Winner!", 'value': ", ".join(winner_list), 'inline': False}
		price = re.sub(r'( • )(Giveaway Has Ended)', r'',gdata['title'])
		gdata['fields'].append(field)

		await ctx.send(f"Giveaway rerolled", hidden=True)
		emojig = self.bot.get_guild(888085276801531967)
		emoji = await emojig.fetch_emoji(893744091710509097)
		emoji2 = await emojig.fetch_emoji(893787497920876544)
		buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", emoji=emoji, disabled=True)]
		await message.edit(embed=embed.from_dict(gdata), components=[create_actionrow(*buttons)])
		await message.reply(
			f"Congratulations {reply}! You won the {price}")

	@cog_ext.cog_slash(name="gdelete", description="Delete a giveaway", guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(name="message_id", description="message id of the giveaway message", required=True, option_type=3),
				create_option(name="channel", description="channel of the giveaway", required=True, option_type=7)
			]
		)
	async def gdelete(self, ctx, message_id:int , channel: discord.TextChannel):

		message = await channel.fetch_message(int(message_id))
		data = await self.bot.give.find_by_custom({'_id': message.id, 'channel': channel.id, 'guild': ctx.guild.id})
		if data is None: return await ctx.send("Ether giveaway is ended or your message id is wrong", hidden=True)
		channel = self.bot.get_channel(data['channel'])
		message = await channel.fetch_message(data['_id'])
		await message.delete()
		await ctx.send("Your giveaway Has been delete", hidden=True)
		await self.bot.give.delete(message.id)
		try:
			self.bot.giveaway.pop(message.id)
		except KeyError:
			pass



def setup(bot):
	bot.add_cog(giveaway(bot))
