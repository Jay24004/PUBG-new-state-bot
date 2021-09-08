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
from amari import AmariClient

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")

time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}
guild_ids=[829615142450495601]

admin_perms = {
	829615142450495601: [
	create_permission(567374379575672852, SlashCommandPermissionType.USER, True),
	create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
	create_permission(829615142450495609, SlashCommandPermissionType.ROLE, True),
	create_permission(829615142450495608, SlashCommandPermissionType.ROLE, True)
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
			print(key, value)
			ftime = value['start_time'] + relativedelta(seconds=value['end_time'])

			if currentTime >= ftime:
				guild = self.bot.get_guild(value['guild'])
				channel = guild.get_channel(value['channel'])
				try:
					message = await channel.fetch_message(int(value['_id']))
				except:
					await self.bot.give.delete(message.id)
					try:
						self.bot.giveaway.pop(message.id)
					except KeyError:
						pass
					return

				data = await self.bot.give.find(message.id)
				host = guild.get_member(value['host'])

				winner_list = []
				users = await message.reactions[0].users().flatten()
				users.pop(users.index(guild.me))

				if len(users) < value['winners']:
					embeds = message.embeds
					for embed in embeds:
						edict = embed.to_dict()

					edict['title'] = f"{edict['title']} • Giveaway Has Ended"
					edict['color'] = 15158332
					edict['description'] = re.sub(r'(Ends)',r'Ended', edict['description'])
					await message.edit(embed=embed.from_dict(edict))
					small_embed = discord.Embed(description=f"No valid [entrants]({message.jump_url}) so the winner could not be determined", color=0x2f3136)
					await message.reply(embed=small_embed)
					await self.bot.give.delete(message.id)
					try:
						self.bot.giveaway.pop((data['_id']))
					except KeyError:
						pass
					return 

				while True:
					member = random.choice(users)
					users.pop(users.index(member))
					winner_list.append(member.mention)
					if len(winner_list) == value['winners']: break

				if len(winner_list) >= value['winners']:
					embeds = message.embeds
					for embed in embeds:
						gdata = embed.to_dict()
					winners = ",".join(winner_list)
					entries = await message.reactions[0].users().flatten()
					small_embed = discord.Embed(description=f"Total Entries: [{len(entries)}]({message.jump_url})")
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
					await message.edit(embed=embed.from_dict(gdata))
					await self.bot.give.delete(message.id)
					try:
						self.bot.giveaway.pop(message.id)
					except KeyError:
						pass

	@check_givaway.before_loop
	async def before_check_givaway(self):
		await self.bot.wait_until_ready()
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} has been loaded \n------")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
		guild = self.bot.get_guild(payload.guild_id)
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		amari_api = AmariClient(self.bot.amari)
		if message.author != self.bot.user: return
		config = await self.bot.config.find(guild.id)
		required = await self.bot.give.find(message.id)
		if required is None:
			return
		try:
			user = await guild.fetch_member(payload.user_id)
		except:
			return

		if user.bot: return

		if config['g_blacklist']:
			for role in config['g_blacklist']:
				role = discord.utils.get(guild.roles, id=role)
				if role in user.roles:
					try:
						embed = discord.Embed(title="Entry Decline",description=f"You have one the blacklist role `{role.name}` there for you cannot enter", color=0xE74C3C)
						await user.send(embed=embed)
						return await message.remove_reaction(payload.emoji, user)
					except discord.HTTPException:
						pass
					return await message.remove_reaction(payload.emoji, user)
		
		if config['g_bypass']:
			for role in config['g_bypass']:
				role = discord.utils.get(guild.roles, id=role)
				if role in user.roles:
					return

		if required['r_req']:
			rrole = discord.utils.get(guild.roles, id=required['r_req'])
			if rrole in user.roles:
				pass
			else:
				if required['b_role']:
					role = discord.utils.get(guild.roles, id=required['b_role'])
					if role in user.roles:
						pass
					else:
						embed = discord.Embed(title="Entry Declined:",
							description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{rrole.name}`",color=0xE74C3C)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
						try:
							await user.send(embed=embed)
						except discord.HTTPException:
							pass
						return await message.remove_reaction(payload.emoji, user)
				else:
					embed = discord.Embed(title="Entry Declined:",
							description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{rrole.name}`",color=0xE74C3C)
					embed.timestamp = datetime.datetime.utcnow()
					embed.set_footer(text=guild.name,icon_url=guild.icon_url)
					try:
						await user.send(embed=embed)
					except discord.HTTPException:
						pass
					return await message.remove_reaction(payload.emoji, user)

		if required['amari_level']:
			user_level = await amari_api.fetch_user(user.guild.id, user.id)
			if user_level.level < required['amari_level']:
				if required['b_role']:
					role = discord.utils.get(guild.roles, id=required['b_role'])
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
						return await message.remove_reaction(payload.emoji, user)
				else:
					embed = discord.Embed(title="Entery Decline:",
						description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:Required amari level to join the giveaway `{required['amari_level']}`", color=0xE74C3C)
					embed.timestamp = datetime.datetime.utcnow()
					embed.set_footer(text=guild.name,icon_url=guild.icon_url)
					try:
						await user.send(embed=embed)
					except discord.HTTPException:
						pass
					return await message.remove_reaction(payload.emoji, user)

		if required['weekly_amari']:
			user_level = await amari_api.fetch_user(user.guild.id, user.id)
			if user_level.weeklyexp < required['weekly_amari']:
				if required['b_role']:
					role = discord.utils.get(guild.roles, id=required['b_role'])
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
						return await message.remove_reaction(payload.emoji, user)
				else:
					embed = discord.Embed(title="Entery Decline:",
						description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:You don't have Required Weekly Amari `{required['weekly_amari']}`", color=0xE74C3C)
					embed.timestamp = datetime.datetime.utcnow()
					embed.set_footer(text=guild.name,icon_url=guild.icon_url)
					try:
						await user.send(embed=embed)
					except discord.HTTPException:
						pass
					return await message.remove_reaction(payload.emoji, user)

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
				create_option(name="ping", description="Ping a role", option_type=8, required=False)
			]
		)
	async def gstart(self, ctx, time, price, winners,required_role=None, bypass_role=None, amari_level: int=None, weekly_amari: int=None, ping:discord.Role=None):
		time = await TimeConverter().convert(ctx, time)
		if time < 15:
			return await ctx.send("Giveaway time needs to be longer than 15 seconds", hidden=True)
		end_time = datetime.datetime.now() + datetime.timedelta(seconds=time)
		end_time = round(end_time.timestamp())
		required_role = required_role if required_role else None
		bypass_role = bypass_role if bypass_role else None
		amari_level = amari_level if amari_level else None
		weekly_amari = weekly_amari if weekly_amari else None

		embed_dict = {'type': 'rich', 'title': price, 'color': 10370047,
		'description': f"React to this message to Enter!!\nEnds: <t:{end_time}:R> (<t:{end_time}:F>)\nHosted By: {ctx.author.mention}", 'fields': []}
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
		msg = await ctx.send(embed=embed.from_dict(embed_dict))

		data = {"_id": msg.id,
				"guild": ctx.guild.id,
				"channel": ctx.channel.id,
				"host": ctx.author.id,
				"winners": winners,
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

		await msg.add_reaction("🎉")
		if ping == None:
			pass
		else:
			await ctx.channel.send(ping.mention)

		await self.bot.give.upsert(data)
		self.bot.giveaway[msg.id] = data

	@cog_ext.cog_slash(name="gend", description="Force end a giveaway", guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(name="message_id", description="message id of the giveaway", required=True, option_type=3)
			]
		)
	async def gend(self, ctx, message_id):
		guild = ctx.guild
		channel = ctx.channel
		message = await channel.fetch_message(int(message_id))
		data = await self.bot.give.find(message.id)
		if data is None: return await ctx.send("I can't Find anything in the Database check your message ID", hidden=True)
		
		host = guild.get_member(data['host'])
		winner_list = []
		users = await message.reactions[0].users().flatten()
		users.pop(users.index(guild.me))
		#try:
			#users.pop(users.index(host))
		#except:
		#	pass

		while len(users) > 0:
			member = random.choice(users)
			users.pop(users.index(member))
			winner_list.append(member.mention)

			if len(winner_list) == data['winners']: break

		if len(users) < data['winners']:
			embeds = message.embeds
			for embed in embeds:
				edict = embed.to_dict()

			edict['title'] = f"{edict['title']} • Giveaway Has Ended"
			edict['description'] = re.sub('Ends', 'Ended', edict['description'])
			edict['color'] = 15158332
			await message.edit(embed=embed.from_dict(edict))
			small_embed = discord.Embed(description=f"No valid [entrants]({message.jump_url})so the winner could not be determined", color=0x2f3136)
			await message.reply(embed=small_embed)
			await ctx.send(embed=small_embed, hidden=True)
			await self.bot.give.delete(message.id)
			try:
				return self.bot.giveaway.pop((data['_id']))
			except KeyError:
				return 

		embeds = message.embeds
		for embed in embeds:
			gdata = embed.to_dict()
		winners = ",".join(winner_list)
		entries = await message.reactions[0].users().flatten()
		small_embed = discord.Embed(description=f"Total Entries: [{len(entries)}]({message.jump_url})")
		await message.reply(
		f"Congratulations {winners}! You won the {gdata['title']}!", embed=small_embed)

		gdata['title'] = f"{gdata['title']} • Giveaway Has Ended"
		gdata['color'] = 15158332
		field = {'name': "Winner!", 'value': ", ".join(winner_list), 'inline': False}
		try:
			gdata['fields'].append(field)
		except KeyError:
			gdata['fields'] = []
			gdata['fields'].append(field)
		await message.edit(embed=embed.from_dict(gdata))
		await ctx.send("Giveaway Ended", hidden=True)
		await self.bot.give.delete(message.id)
		try:
			self.bot.giveaway.pop(message.id)
		except KeyError:
			pass

	@cog_ext.cog_slash(name="greroll", description="Reroll the giveaway for new winners",guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
			create_option(name="message_id", description="message id of the giveaway", required=True, option_type=3),
			create_option(name="winners", description="numbers of winners", required=True, option_type=4),
			create_option(name="channel", description="channel of giveaway message", required=False, option_type=7),
			]
		)
	async def greroll(self, ctx, message_id, winners: int, channel=None,):
		message_id = int(message_id)
		channel = channel if channel else ctx.channel
		message = await channel.fetch_message(message_id)

		if message.author.id != self.bot.user.id:
			return await ctx.send("That message is not an giveaway", hidden=True)

		users = await message.reactions[0].users().flatten()
		users.pop(users.index(ctx.guild.me))
		entries = await message.reactions[0].users().flatten()
		entries.pop(entries.index(ctx.guild.me))

		if len(users) == 0: return await ctx.send("No winner found as there no reactions", hidden=True)
		if len(users) < winners: return await ctx.send(f"no winners found as there no reactions to meet {winners} requirment", hidden=True)
		
		winner_list = []
		while True:
			member = random.choice(users)
			if type(member) == discord.Member:
				users.pop(users.index(member))
				winner_list.append(member.mention)
			else:
				pass
			if len(winner_list) == winners:
				break

		reply = ",".join(winner_list)
		embeds = message.embeds
		for embed in embeds:
			gdata = embed.to_dict()

		gdata['fields'] = []
		gdata['color'] = 15158332
		field = {'name': "Winner!", 'value': ", ".join(winner_list), 'inline': False}
		price = re.sub(r'( • )(Giveaway Has Ended)', r'',gdata['title'])
		gdata['fields'].append(field)

		await ctx.send(f"**Price**: {price}\n**Winners**: {reply}\n**Total Entries**: {len(entries)}", hidden=True)
		await message.edit(embed=embed.from_dict(gdata))
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

	@cog_ext.cog_slash(name="setblacklist", description="Blacklist role from giveaway it's an Server whide blacklist",guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(name="role", description="Select role to blacklist it if it's already blacklist it's will remove it", required=True, option_type=8)
			]
		)
	async def gblacklist(self, ctx, role):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None: return await ctx.send("Your Server config was not found please run config First")
		if role.id in data['g_blacklist']:
			data['g_blacklist'].remove(role.id)
			return await ctx.send(f"{role.mention} Has been Removed from blacklist ", hidden=True)
		else:	
			data['g_blacklist'].append(role.id)
		await self.bot.config.upsert(data)
		await ctx.send(f"{role.mention} Has added to Blacklist", hidden=True)

	@cog_ext.cog_slash(name="setbypass", description="make and role to bpyass all global giveaway",guild_ids=guild_ids,default_permission=False,
		permissions=admin_perms,
		options=[
				create_option(name="role", description="Select role make it bypass, if already bypass role it's will remove it", required=True, option_type=8)
			]
		)
	async def gbypass(self, ctx, role: discord.role):
		data = await self.bot.config.find(ctx.guild.id)
		if data is None: return await ctx.send("Your Server config was not found please run config First")
		if role.id in data['g_bypass']:
			data['g_bypass'].remove(role.id)
			await ctx.send(f"{role.mention} Has been Removed from the Bypass list", hidden=True)
			return await self.bot.config.upsert(data)
		await self.bot.config.upsert(data)
		await ctx.send(f"{role.mention} is added to bypass list", hidden=True)

	@cog_ext.cog_slash(name="bypasslist", description="Send the Bypass role list", guild_ids=guild_ids, default_permission=False, permissions=admin_perms)
	async def bypasslist(self, ctx):
		data = await self.bot.config.find(ctx.guild.id)
		lists = []
		for role in data['g_bypass']:
			role = discord.utils.get(ctx.guild.roles, id=role)
			lists.append(role.mention)

		embed = discord.Embed(title="Bypass Role list", description=", ".join(lists), color=0x2f3136)

		await ctx.send(embed=embed, hidden=False)

	@cog_ext.cog_slash(name="blacklist", description="Send the blacklist role list", guild_ids=guild_ids, default_permission=False, permissions=admin_perms)
	async def blacklistl(self, ctx):
		data = await self.bot.config.find(ctx.guild.id)
		lists = []
		for role in data['g_blacklist']:
			role = discord.utils.get(ctx.guild.roles, id=role)
			lists.append(role.mention)

		embed = discord.Embed(title="blacklist Role list", description=", ".join(lists), color=0x2f3136)
		await ctx.send(embed=embed)	

def setup(bot):
	bot.add_cog(giveaway(bot))
