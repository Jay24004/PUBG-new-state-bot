import datetime
import discord

from copy import deepcopy
from humanfriendly import format_timespan
from dateutil.relativedelta import relativedelta
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

from discord.ext import tasks, commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_task = self.check_current_mutes.start()
        self.ban_task = self.check_current_bans.start()
        self.count_task = self.change_status.start()


    def cog_unload(self):
            self.mute_task.cancel()

    def cog_unload(self):
        self.ban_task.cancel()

    def cog_unload(self):
        self.count_task.cancel()

    @tasks.loop(seconds=240)
    async def change_status(self):      
        guild = self.bot.get_guild(785839283847954433)
        members = guild.members
        count = 0
        for i in members:
            if i.bot:
                count = count + 1
        
        member = guild.member_count - count
        activity = f'over {member} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"),status= discord.Status.dnd)


    @tasks.loop(seconds=10)
    async def check_current_mutes(self):
        currentTime = datetime.datetime.now()
        mutes = deepcopy(self.bot.muted_users)
        for key, value in mutes.items():
            if value['muteDuration'] is None:
                continue

            unmuteTime = value['mutedAt'] + relativedelta(seconds=value['muteDuration'])

            if currentTime >= unmuteTime:
                guild = self.bot.get_guild(value['guildId'])
                member = guild.get_member(value['_id'])

                if member is None:
                    await self.bot.mutes.delete(value['_id'])    
                    try:
                        self.bot.muted_users.pop(value['_id'])
                    except KeyError:
                        return

                role = discord.utils.get(guild.roles, name="Muted")
                if role in member.roles:
                    await member.remove_roles(role)


                    log_channel = self.bot.get_channel(855784930494775296)
                    data = await self.bot.config.find(guild.id)
                    log_embed = discord.Embed(title=f"🔊 UnMute | Case ID: {data['case']}",
                    	description=f"**Offender**: {member.name} | {member.mention} \n**Moderator**: {self.bot.user.name} | {self.bot.user.mention} \n**Reason**: Temporary Mute expired", color=0x2ECC71)
                    log_embed.set_thumbnail(url=member.avatar_url)
                    log_embed.timestamp = datetime.datetime.utcnow()
                    log_embed.set_footer(text=f"ID: {member.id}")

                    await log_channel.send(embed=log_embed)

                    data["case"] += 1
                    await self.bot.config.upsert(data)

                await self.bot.mutes.delete(member.id)
                try:
                    self.bot.muted_users.pop(member.id)
                except KeyError:
                    pass#🔓

    @tasks.loop(seconds=10)
    async def check_current_bans(self):
        currentTime = datetime.datetime.now()
        bans = deepcopy(self.bot.ban_users)
        for key, value in bans.items():
            if value['BanDuration'] is None:
                continue

            unbanTime = value['BannedAt'] + relativedelta(seconds=value['BanDuration'])

            if currentTime >= unbanTime:
                guild = self.bot.get_guild(value['guildId'])
                member = await self.bot.fetch_user(int(value['_id']))
                reason = "Temporary Ban expired"
                try:
                    await guild.unban(member, reason=reason)
                except:
                    pass

                case = await self.bot.config.find(guild.id)
                log_channel = self.bot.get_channel(855784930494775296)

                log_embed = discord.Embed(title=f"🔓 UnBan | Case ID: {case['case']}",
                description=f" **Offender**: {member.name} | {member.mention}\n**Reason** {reason}:\n**Moderator**: {self.bot.user.name} {self.bot.user.mention}", color=0x2ECC71)
                log_embed.set_thumbnail(url=member.avatar_url)
                log_embed.set_footer(text=f"ID: {member.id}")
                log_embed.timestamp = datetime.datetime.utcnow()
                await log_channel.send(embed=log_embed)

                case["case"] += 1
                await self.bot.config.upsert(case)

                await self.bot.bans.delete(member.id)
            try:
                self.bot.ban_users.pop(member.id)
            except KeyError:
                pass


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    
    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, ex):
        if isinstance(ex, commands.MissingPermissions):
            await ctx.send("Hey! You lack permission to use this command.")
        elif isinstance(ex, commands.MissingAnyRole):
            await ctx.send("Hey! You lack permission to use this command.")
        else:
            embed = discord.Embed(color=0xE74C3C, 
                description=f"Error: `{ex}`")
            await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Events(bot))