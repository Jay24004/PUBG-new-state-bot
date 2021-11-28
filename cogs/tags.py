import discord
from discord import user
from discord.ext import commands
from discord.ext.commands.core import check, guild_only
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
import asyncio
import datetime
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from utils.util import Pag
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.context import ComponentContext

guild_ids=[814374218602512395]

perms_a = {
    814374218602512395: [
        create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
        create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
        create_permission(909333702683799562, SlashCommandPermissionType.ROLE, True)
    ]
}

perms_staff = {
    814374218602512395: [
        create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
        create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
        create_permission(909333702683799562, SlashCommandPermissionType.ROLE, True),
        create_permission(814405684581236774, SlashCommandPermissionType.ROLE, True)
    ]
}

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog is ready')
    

    @cog_ext.cog_subcommand(base="Tag", name="create", description="Create New tag", guild_ids=guild_ids, base_default_permission=False, base_permissions=perms_a,
        options=[
            create_option(name="tag_name", description="Enter Tag Name", required=True, option_type=3)
        ])
    async def create(self, ctx, tag_name:str):
        await ctx.defer()
        await ctx.channel.send("Enter Your Tag Message")
        try:
            msg = await self.bot.wait_for('message', check= lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send('TimeoutError')
        tag_filter = {'tag_name': tag_name, 'guildID': ctx.guild.id}
        tag_data = {'made_by': ctx.author.id, 'tag_messsage': msg.content, 'time': datetime.datetime.now()}

        await self.bot.tags.update_by_custom(tag_filter, tag_data)
        data = await self.bot.tags.find_by_custom({'tag_name': tag_name, 'guildID': ctx.guild.id})
        embed = discord.Embed(description=f"```py\n{data}\n```")
        await ctx.send(embed=embed)
    
    @cog_ext.cog_subcommand(base="tag", name="use", description="user tag", guild_ids=guild_ids, base_default_permission=False, base_permissions=perms_staff,)
    async def use(self, ctx, tag_name ,users:str=None, channel:str=None, extra:str=None):
        await ctx.defer(hidden=True)
        data = await self.bot.tags.find_by_custom({'tag_name': tag_name, 'guildID': ctx.guild.id})
        if not data: return await ctx.send(f"No tag Found with name `{tag_name}`")
        message = data['tag_messsage']

        if users:
            message = message.replace('{users}', f'{users}')
        else:
            message = message.replace('{users}', f'')

        if channel:
            message = message.replace('{channel}', f'{channel}')
        else:
            message = message.replace('{channel}', f'')
        
        if extra:
            message = message.replace('{extra}', f'{extra}')
        else:
            message = message.replace('{extra}', f'')
        await ctx.channel.send(message)
        await ctx.send(f"You used tags named with {tag_name} in {ctx.channel.mention}", hidden=True)
    
    @cog_ext.cog_subcommand(base="Tag", description="Show list of all tags", name="list", guild_ids=guild_ids, base_default_permission=False, base_permissions=perms_staff)
    async def _list(self, ctx):
        await ctx.defer()
        tag_filter = {'guildID': ctx.guild.id}
        data = await self.bot.tags.find_many_by_custom(tag_filter)
        if not data: return await ctx.send("No Tags Found for this server.", hidden=True)
        pages = []
        for tags in data:
            description=f"""
            **Tage Name**: {tags['tag_name']}
            **Tage Message**: {tags['tag_messsage']}
            **Tage Made by**: <@{tags['made_by']}>
            """
            pages.append(description)
        
        await Pag(title=f"Tags list for {ctx.guild.name}", color=0x11eca4, length=1, entries=pages).start(ctx)

    @cog_ext.cog_subcommand(base="Tag", description="Edit an tag text", name="edit", guild_ids=guild_ids, base_default_permission=False, base_permissions=perms_a)
    async def edit(self, ctx, tag_name:str):
        await ctx.defer()
        data =  await self.bot.tags.find_by_custom({'tag_name': tag_name, 'guildID': ctx.guild.id})
        if not data: return await ctx.send(f"No tag found with name of `{tag_name}`")
        await ctx.channel.send("Enter New Tag message")
        try:
            msg = await self.bot.wait_for('message', check= lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        except:
            return await ctx.send("TimeoutError")
        
        await msg.add_reaction("✅")
        embed = discord.Embed(title=f"Editing Tag {tag_name}", description=f"Are you sure you want to edit the tag `{tag_name}`",color=0xff0000)
        embed.add_field(name="New Message:", value=msg.content)
        embed.add_field(name="Old Message:", value=data['tag_messsage'],inline=False)
        embed.timestamp = datetime.datetime.now()
        buttons = [create_button(style=ButtonStyle.green, label="Yes", disabled=False), create_button(style=ButtonStyle.blurple, label="No", disabled=False)]
        config = await ctx.send(embed=embed, components=[create_actionrow(*buttons)])
        try:
            res: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(*buttons)], check=lambda button_ctx: button_ctx.author == ctx.author, timeout=60)
            if res.component['label'].lower() == "yes":
                data['tag_messsage'] = msg.content
                await self.bot.tags.upsert(data)
                buttons = [create_button(style=ButtonStyle.green, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                await res.send('Your tag is updated', hidden=True)
                return await config.edit(components=[create_actionrow(*buttons)])

            if res.component['label'].lower() == "no":
                await res.send('no changes where made', hidden=True)
                return await config.edit(content="Let me know you want to update the tag",embed=None, components=[create_actionrow(*buttons)])

        except asyncio.TimeoutError:

            buttons = [create_button(style=ButtonStyle.green, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
            await config.edit(content="TimeOut Error", components=[create_actionrow(*buttons)])
    
    @cog_ext.cog_subcommand(base="Tag", name="Info", description="Show help command for the creating tags", guild_ids=guild_ids, base_default_permission=False, base_permissions=perms_staff)
    async def info(self, ctx):
        embed = discord.Embed(title="How to Use Tags", color=0x11eca4, description="ㅤㅤ\n")
        embed.add_field(name="How to Make Tag:",value="1. Select `/tagm create` command from list\n\n2. Select `tag_name` field and enter tag name\n\n3. Select `tag_message` field and enter your text.\n> To add mentions in tags add `{users}`\n> for channel `{channel}`, Extra info `{extra}`")
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name="How to Use Tag", value="1. Select `<tag>` command from list\n\n2. Enter tag name in `tag` field use `/tag list` get all tags list\n\n2. Enter users mention, channels mention and Extra info in `{users}, {channel}, {extra}` in appropriate field")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Tags(bot))

