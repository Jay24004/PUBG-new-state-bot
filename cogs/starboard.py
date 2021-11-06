import re
import discord
import asyncio
import datetime
from discord import channel
from discord.enums import Theme
from discord.ext import commands
from utils.exceptions import IdNotFound
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

staff_perm = {
    814374218602512395:[
        create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
        create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
    ],
    829615142450495601:[
        create_permission(829615142450495601, SlashCommandPermissionType.ROLE, True),
        create_permission(829615142450495609, SlashCommandPermissionType.ROLE, True),
        create_permission(829615142672531459, SlashCommandPermissionType.ROLE, True),
    ]
}

guild_ids = [814374218602512395, 829615142450495601]

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_read(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id:
            return
        entries = await self.bot.config.get_all()
        guilds = list(map(lambda e: e["_id"], entries))
        if payload.guild_id in guilds:
            guild = list(filter(lambda e: e["_id"] == payload.guild_id, entries))
            guild = guild[0]
            emoji = "⭐"
        if not guild.get("starboard_channel"): return    
        if not guild.get("starboard_toggle", True): return
        if not str(payload.emoji) == "⭐": return

        channel = self.bot.get_channel(payload.channel_id)
        try:
            msg = await channel.fetch_message(payload.message_id)
            reacts = msg.reactions
            reacts = list(filter(lambda r: str(r.emoji) == "⭐", reacts))
        except discord.HTTPException:
            channel = self.bot.get_channel(893057761607315496)
            return await channel.send("An Error has happpens when getting message")

        if reacts:
            react = list(map(lambda u: u.id, await reacts[0].users().flatten()))
            if msg.author.id in react:
                del react[react.index(msg.author.id)]
            
            thresh = guild.get("emoji_threshold") or 7
            if len(react) >= thresh:
                starboard_channel = self.bot.get_channel(guild["starboard_channel"])
                try:
                    existing_star = await self.bot.starboard.find_by_custom(
                                    {
                                        "_id": payload.message_id,
                                        "guildId": payload.guild_id,
                                        "channelId": payload.channel_id,
                                    }
                                )
                except IdNotFound:
                    pass
                
                else:
                    if not existing_star:
                        pass
                    else:
                        existing_message = await starboard_channel.fetch_message(existing_star["starboard_message_id"])
                        return await existing_message.edit(content=f":dizzy: {len(react)} | {channel.mention}",embed=existing_message.embeds[0])
                                            
                if channel == starboard_channel: return

                embed = discord.Embed(description=msg.content,color=0x11eca4, timestamp=datetime.datetime.now())
                embed.set_author(name=f"{msg.author.display_name}",icon_url=msg.author.avatar_url)
                embed.set_footer(text=f"ID: {msg.id}")
                embed.add_field(name="Original", value=f"[Jump!]({msg.jump_url})")
                if msg.reference:
                    reply_to = await channel.fetch_message(msg.reference.message_id)
                    if not reply_to:
                        pass
                    else:
                        embed.add_field(name="Replying to...", value=f"[{reply_to.author.display_name}]({reply_to.jump_url})", inline=False)
                
                attach = msg.attachments[0] if msg.attachments else None
                if attach:
                    embed.set_image(url=attach.url)
                
                starboard_message =  await starboard_channel.send(content=f":dizzy: {len(react)} | {channel.mention}",embed=embed)
                await starboard_message.add_reaction("⭐")
                await self.bot.starboard.upsert(
                    {"_id": payload.message_id,
                    "guildId": payload.guild_id,
                    "authorId": payload.user_id,
                    "channelId": payload.channel_id,
                    "starboard_message_id": starboard_message.id,}
                )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if not payload.guild_id: return
        entries = await self.bot.config.get_all()
        guilds = list(map(lambda e: e["_id"], entries))
        if payload.guild_id in guilds:
            guild = list(filter(lambda e: e["_id"] == payload.guild_id, entries))
            guild = guild[0]
            emoji = "⭐"
        
        if not guild.get("starboard_channel"): return

        if not guild.get("starboard_toggle", True): return

        if str(payload.emoji) == emoji:
            channel = self.bot.get_channel(payload.channel_id)
            try:
                msg = await channel.fetch_message(payload.message_id)
                reacts = msg.reactions
                reacts = list(filter(lambda r: str(r.emoji) == emoji, reacts))
            except discord.HTTPException:
                channel = self.bot.get_channel(893057761607315496)
                return await channel.send("An Error has happpens when getting message")
            
            if reacts:
                react = list(map(lambda u: u.id, await reacts[0].users().flatten()))
                if msg.author.id in react:
                    del react[react.index(msg.author.id)]

                thresh = guild.get("emoji_threshold") or 7
                if len(react) >= thresh:
                    starboard = self.bot.get_channel(guild["starboard_channel"])
                    try:
                        existing_star = await self.bot.starboard.find_by_custom(
                            {
                                "_id": payload.message_id,
                                "guildId": payload.guild_id,
                                "channelId": payload.channel_id,
                            }
                        )
                    except IdNotFound:
                        return
                    else:
                        if not existing_star.get("starboard_message_id"):
                            return
                        existing_message = await starboard.fetch_message(existing_star["starboard_message_id"])
                        return await existing_message.edit(content=f":dizzy: {len(react)} | {channel.mention}",embed=existing_message.embeds[0])

    @cog_ext.cog_slash(name="starboard", description="Config command for startbord module", default_permission=False, permissions=staff_perm, guild_ids=guild_ids,
    options=[
        create_option(name="toggle", description="Toggle the starbord", required=False, option_type=5),
        create_option(name="threshold", description="Set threshhold for the reactions", required=False, option_type=4),
        create_option(name="channel", description="Set Channel for Starbord", required=False, option_type=7),
    ])
    async def starbord(self, ctx, toggle: bool=None, threshold:int=None, channel:discord.TextChannel=None):
        data = await self.bot.config.find(ctx.guild.id)        
        if toggle:
            data['starboard_toggle'] = toggle
        if threshold:
            data['emoji_threshold'] = threshold
        if channel:
            data['starboard_channel'] = channel.id
        await self.bot.config.upsert(data)
        embed = discord.Embed(title=f"{ctx.guild.name}'s Startbord Config",color=0x11eca4,
        description=f"ㅤ\nStartbord Toggle: {data['starboard_toggle']}\nStarbord Channel: <#{data['starboard_channel']}>\nStartboard Threshold: {data['emoji_threshold']}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed, hidden=False)

def setup(bot):
    bot.add_cog(starboard(bot))
        

            
