import asyncio
from logging import disable
import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only
from discord_slash.model import SlashCommandPermissionType
from discord_together import DiscordTogether
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash import cog_ext, cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, create_select, create_select_option
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle
permission = {
    814374218602512395: [
        create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
        create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
        create_permission(814405684581236774, SlashCommandPermissionType.ROLE, True),
        create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
        create_permission(816595613230694460, SlashCommandPermissionType.ROLE, True),
    ]
}

guild_ids = [814374218602512395]

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):        
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')
    
    @cog_ext.cog_slash(name="activity", description="Discord Voice Games", guild_ids=guild_ids)
    async def activity(self, ctx):
        if ctx.author.voice == None: return await ctx.send("Please Join Voice channel", hidden=True)
        buttons =[
                create_button(style=ButtonStyle.green,label="youtube"),
                create_button(style=ButtonStyle.green,label="chess"),
                create_button(style=ButtonStyle.green,label="fishing"),
                create_button(style=ButtonStyle.green,label="word-snack"),
                create_button(style=ButtonStyle.green,label="doodle-crew")]
        embed = discord.Embed(title="Note",color=ctx.author.color, description="This Activitys are still in beta it's tends to creash sometimes\nLink is only vaild for 60s")
        message = await ctx.send(embed=embed, components=[create_actionrow(*buttons)])
        try:
            res: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(*buttons)], check=lambda button_ctx: button_ctx.author == ctx.author, timeout=60)
            link = await self.bot.togetherControl.create_link(ctx.author.voice.channel.id, res.component['label'].lower(), max_age=60, max_uses=10)
            link_button = [create_button(style=ButtonStyle.URL, label="Start", url=link)]
            return await res.edit_origin(embed=embed, components=[create_actionrow(*link_button)])            
        except asyncio.TimeoutError:
            await message.delete()

def setup(bot):
    bot.add_cog(Activity(bot))