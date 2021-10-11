import discord
from discord.ext import commands
import re
import datetime


bad_word = ['aand', 'aandu', 'balatkar', 'beti chod', 'bhadva', 'bhadve', 'bhandve', 'bhootni ke', 'bhosad', 'bhosadi ke', 'boobe', 'chinki', 'chod', 'chodu', 'chodu bhagat', 'chooche', 'choochi', 'choot', 'choot ke baal', 'chootia', 'chootiya', 'chuche', 'chuchi', 'chudai khanaa', 'chudan chudai', 'chut', 'chut ke baal', 'chut ke dhakkan', 'chut maarli', 'chutad', 'chutadd', 'chutan', 'chutia', 'chutiya', 'gaand', 'gaandfat', 'gaandmasti', 'gaandufad', 'gandu', 'gashti', 'gasti', 'ghassa', 'ghasti', 'haramzade', 'hawas', 'hawas ke pujari', 'hijda', 'hijra', 'jhant', 'jhant chaatu', 'jhant ke baal', 'jhantu', 'kamine', 'kaminey', 'kanjar', 'kutta kamina', 'kutte ki aulad', 'kutte ki jat', 'kuttiya', 'loda', 'lodu', 'lund', 'lund choos', 'lund khajoor', 'lundtopi', 'lundure', 'maa ki chut', 'madar chod', 'mooh mein le', 'mutth', 'raand', 'randi', 'kutti', 'randi', 'tatte', 'bhosada', 'chut', 'harak', 'anal', 'anus', 'arse', 'ass', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'blow job', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'cunt', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'f u c k', 'fudgepacker', 'fudge packer', 'flange', 'homo', 'jerk', 'jizz', 'knobend', 'knob end', 'labia', 'muff', 'nigger', 'nigga', 'penis', 'prick', 'pube', 'pussy', 'queer', 'scrotum', 'sex', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore', 'bisi', 'lode', 'Bcmc', 'lovde', 'chutiya', 'chutiye', 'madherchod', 'benchod', 'bcmc', 'madarchod', 'madrchod', 'madrchd', 'bhenchod', 'gandu', 'lund', 'lunn', 'lun', 'hutiya', 'chutchoot', 'chumtiya', 'chuntia', 'chutia', 'fucker', 'sucker', 'dickhead', 'asshole', 'niga', 'Niga', 'Nigga', '%bc%', 'gai', 'gea']

bad_regex = re.compile(r'\b(?:%s)\b' % '|',join(bad_word), flags=re.I|re.M)
invite_regex = re.compile(r"((?:https?://)?discord(?:app)?\.(?:com/invite|gg|io|me|li|)/( |)[a-zA-Z0-9]+/?)|((|gg|io|me|li|)( |)([a-zA-Z0-9]+/?))", flags=re.I|re.M,)
links_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
class profanity(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot: return
		if message.guild.id == 814374218602512395:
			if message.channeln.id in [814381412210704415, 814381619581943828,886589931324076083,887247296721457192]: return
			match = re.findall(links_regex, message.content)
			if match:
				links = ",".join([x[0] for x in match])
				embed = discord.Embed(title=f"{message.author.name}", description=f"Message: {message.content}\nChannel: {message.channel.mention}\nLinks:{links}", color=0x2f3136)
				embed.set_footer(text=f"ID: {message.author.id}", icon_url=message.author.avatar_url)
				embed.timestamp = datetime.datetime.now()
				embed.set_thumbnail(url=message.author.avatar_url)
				await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(profanity(bot))