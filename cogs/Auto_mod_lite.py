import discord
from discord.ext import commands
import re
import requests
import json
import datetime

def is_link_there(str: str):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,str)
    return [x[0] for x in url]

def is_link_bad(link: str):
    url = f"https://bad-domains.walshy.dev/check"
    payload= {"domain": link}
    r = requests.post(url, data=json.dumps(payload)).json()
    return r

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.automod != True: return
        if message.author.bot: return
        if message.guild.id != 829615142450495601 or 814374218602512395: return

        link = is_link_there(message.content)
        if len(link) > 0:
            r = is_link_bad(link[0])
            if r['badDomain'] == True:
                role = discord.utils.get(message.guild.roles, name="Muted")
                await message.author.add_roles(role)

                embed = discord.Embed(description=f"Message Sent by {message.author.mention} Contains known phishing link",color=0xff0000)
                embed.add_field(name="Message", value=f"||{message.content}||")
                embed.add_field(name="Action Taken", value="Timeout User For 1 Day")
                embed.set_footer(text=message.author.id)

                if message.guild.id == 814374218602512395:
                    channel = self.bot.get_channel(886881989150531605)
                    await message.delete()
                    await channel.send(embed=embed, content="<@&814405684581236774> If link is phishing ban user Fast")
                    try:
                        await message.author.send("phishing has been detected in your message and you have been put on timeout if you think it's mistake Dm any Admin")
                    except:
                        pass
                if message.guild.id == 829615142450495601:
                    channel = self.bot.get_channel(882593915360935936)
                    await message.delete()
                    await channel.send(embed=embed, content="<@&894124699527815188> If link is phishing ban user Fast")
                    try:
                        await message.author.send("phishing has been detected in your message and you have been put on timeout if you think it's mistake Dm any Admin")
                    except:
                        pass

def setup(bot):
    bot.add_cog(AutoMod(bot))