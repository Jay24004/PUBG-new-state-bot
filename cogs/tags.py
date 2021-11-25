import asyncio
from datetime import datetime
import re
from typing_extensions import Required
import discord
import datetime
from discord import guild
from discord import embeds
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.context import ComponentContext
from utils.util import Pag
import re
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

guild_ids=[814374218602512395]

admin_perms = {
    814374218602512395:
    [
        create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
        create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
    ]
}

staff_perms = {
    814374218602512395:

    [   
        create_permission(894123602918670346, SlashCommandPermissionType.ROLE, True),
        create_permission(814405582177435658, SlashCommandPermissionType.ROLE, True),
        create_permission(814405684581236774, SlashCommandPermissionType.ROLE, True),
        create_permission(816595613230694460, SlashCommandPermissionType.ROLE, True)
    ]
}
class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is Ready")
    
    @cog_ext.cog_subcommand(base="TagM", name="create", description="Create New Tag", guild_ids=guild_ids, base_default_permission=False,base_permissions=admin_perms, 
        options=[
            create_option(name="tag_name", description="Give tag an name", required=True, option_type=3),
            create_option(name="tag_message", description="Enter Tag message", required=True, option_type=3)
        ])
    async def create(self, ctx, tag_name, tag_message):
        tag_filter = {'tag_name': tag_name, 'tag_guildId': ctx.guild.id}
        result = await self.bot.tags.find_many_by_custom(tag_filter)
        if result: return await ctx.send("There an tag already in database with this make use `/tag list` to ckeck all tags", hidden=True)

        tag_data = {'tag_message': tag_message, 'tag_creater': ctx.author.id, 'tag_createAt': datetime.datetime.utcnow()}
        await self.bot.tags.update_by_custom(tag_filter, tag_data)
        await ctx.send("Your tag is add to the database")

    @cog_ext.cog_subcommand(base="Tag", name="list", description="Show list of all tags of the server", guild_ids=guild_ids, base_default_permission=False, base_permissions=staff_perms)
    async def list(self, ctx):
        tag_filter = {'tag_guildId': ctx.guild.id}
        data = await self.bot.tags.find_many_by_custom(tag_filter)
        if not data: return await ctx.send("There is no tag for this server", hidden=True)
        pages = []
        for tag in data:
            user = self.bot.get_user(tag['tag_creater'])
            description=f"""
            Tag Name: {tag['tag_name']}
            Tag made by: {user.name}
            Tag Message: `{tag['tag_message']}`
            Tag Created at: {tag['tag_createAt'].strftime("%I:%M %p %B %d, %Y")}
            """
            pages.append(description)
        
        await Pag(title=f"List of Tags for {ctx.guild.name}", color=0x09f507, entries=pages, length=1).start(ctx)

    @cog_ext.cog_subcommand(base="Tag", description="Use tags", guild_ids=guild_ids, base_default_permission=False, base_permissions=staff_perms,
        options=[
            create_option("tag", description="Enter name of tag", option_type=3, required=True),
            create_option("users", description="Enter user mentions if needed", option_type=3, required=False),
            create_option("channel", description="Enter channel mentions if needed", option_type=3, required=False),
            create_option("extra", description="Enter extra information if needed or leave it empty", option_type=3, required=False),
        ])
    async def tag(self, ctx, tag, users: str=None, channel: str=None, extra: str=None):
        tag_filter = {'tag_name': tag, 'tag_guildId': ctx.guild.id}
        data = await self.bot.tags.find_by_custom(tag_filter)
        if not data: return await ctx.send("Please check your tag name there is no tag in databse with this name", hidden=True)
        if users:
            new_message = data['tag_message'].replace('{users}', f'{users}')
        else:
            new_message = data['tag_message'].replace('{users}', '')
        
        if channel:
            new_message = new_message.replace('{channel}', f'{channel}')
        else:
            new_message = new_message.replace('{channel}', f'')
        
        if extra:
            new_message = new_message.replace('{extra}', f'{extra}')
        else:
            new_message = new_message.replace('{extra}', f'')        

        await ctx.send("Done tag sended", hidden=True)

        await ctx.channel.send(new_message)

    @cog_ext.cog_subcommand(base="Tag", name="Info", description="Show help command for the creating tags", guild_ids=guild_ids, base_default_permission=False)
    async def info(self, ctx):
        embed = discord.Embed(title="How to Use Tags", color=0x11eca4, description="ㅤㅤ\n")
        embed.add_field(name="How to Make Tag:",value="1. Select `/tagm create` command from list\n\n2. Select `tag_name` field and enter tag name\n\n3. Select `tag_message` field and enter your text.\n> To add mentions in tags add `{users}`\n> for channel `{channel}`, Extra info `{extra}`")
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name="How to Use Tag", value="1. Select `<tag>` command from list\n\n2. Enter tag name in `tag` field use `/tag list` get all tags list\n\n2. Enter users mention, channels mention and Extra info in `{users}, {channel}, {extra}` in appropriate field")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="TagM", name="edit", description="edit an tag", guild_ids=guild_ids, base_default_permission=False, base_permissions=admin_perms,
        options=[
            create_option(name="tag_name", description="Enter Tag Name", option_type=3, required=True),
            create_option(name="new_message", description="Enter new Message for the tag", option_type=3, required=False),
            create_option(name="remove_tag", description="Select this to delete tag", option_type=5, required=False)
        ])
    async def edit(self, ctx,tag_name: str, new_message=None,remove_tag: bool=None):
        tag_filter = {'tag_name': tag_name, 'tag_guildId': ctx.guild.id}
        data = await self.bot.tags.find_by_custom(tag_filter)
        if not data: return await ctx.send(f"No tag found with `{tag_name}` try `/tag list` to get list of all tags")

        if remove_tag == True:

            buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=False), create_button(style=ButtonStyle.blurple, label="No", disabled=False)]

            embed = discord.Embed(description=f"Are you sure you want to delete this tag\nTag Name: {data['tag_name']}\nTag Message: {data['tag_message']}\nMade by: <@{data['tag_creater']}>",color=0xff0000)

            msg = await ctx.send(embed=embed, components=[create_actionrow(*buttons)], hidden=False)
            while True:
                try:
                    button_ctx: ComponentContext = await wait_for_component(self.bot, components=create_actionrow(*buttons), timeout=10)

                    if button_ctx.author == ctx.author:

                        if button_ctx.component['label'].lower() == "yes":
                            await self.bot.tags.delete(data['_id'])
                            await button_ctx.edit_origin(content="Tag has been deleted", components=None)
                            buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                            await msg.edit(components=[create_actionrow(*buttons)])
                            return
                        
                        if button_ctx.component['label'].lower() == "no":
                            buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                            await msg.edit(components=[create_actionrow(*buttons)])
                            return
                    else:
                        await ctx.send("This is not your button")
                except asyncio.TimeoutError:
                    buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                    await msg.edit(components=[create_actionrow(*buttons)])
                    break
            return

        if new_message:        

            embed = discord.Embed(description=f"Are you sure you want to edit the tag `{tag_name}`",color=0xff0000)
            embed.add_field(name="New Message", value=new_message)
            embed.add_field(name="Old Message", value=data['tag_message'], inline=False)

            buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=False), create_button(style=ButtonStyle.blurple, label="No", disabled=False)]
            msg = await ctx.send(embed=embed, components=[create_actionrow(*buttons)])

            while True:
                try:
                    button_ctx: ComponentContext = await wait_for_component(self.bot, components=create_actionrow(*buttons), timeout=10)
                    if button_ctx.author == ctx.author:
                        if button_ctx.component['label'].lower() == "yes":
                            data['tag_message'] = new_message
                            await self.bot.tags.upsert(data)
                            await button_ctx.send('Tags has been updated',hidden=False)
                            buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                            return await msg.edit(components=[create_actionrow(*buttons)])
                        if button_ctx.component['label'].lower() == "no":
                            await ctx.send("command is cancelled")
                            buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                            return await msg.edit(components=[create_actionrow(*buttons)])
                    else:
                        await button_ctx.send("This buttons are not for your", hidden=True)
                except asyncio.TimeoutError:
                        buttons = [create_button(style=ButtonStyle.red, label="Yes", disabled=True), create_button(style=ButtonStyle.blurple, label="No", disabled=True)]
                        return await msg.edit(content="Timeouted",components=[create_actionrow(*buttons)])
def setup(bot):
    bot.add_cog(tags(bot))
