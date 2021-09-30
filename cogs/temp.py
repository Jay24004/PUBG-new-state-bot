import discord
from discord.ext import commands

import datetime


bad_word = ['aand', 'aandu', 'balatkar', 'beti chod', 'bhadva', 'bhadve', 'bhandve', 'bhootni ke', 'bhosad', 'bhosadi ke', 'boobe', 'chinki', 'chod', 'chodu', 'chodu bhagat', 'chooche', 'choochi', 'choot', 'choot ke baal', 'chootia', 'chootiya', 'chuche', 'chuchi', 'chudai khanaa', 'chudan chudai', 'chut', 'chut ke baal', 'chut ke dhakkan', 'chut maarli', 'chutad', 'chutadd', 'chutan', 'chutia', 'chutiya', 'gaand', 'gaandfat', 'gaandmasti', 'gaandufad', 'gandu', 'gashti', 'gasti', 'ghassa', 'ghasti', 'harami', 'haramzade', 'hawas', 'hawas ke pujari', 'hijda', 'hijra', 'jhant', 'jhant chaatu', 'jhant ke baal', 'jhantu', 'kamine', 'kaminey', 'kanjar', 'kutta', 'kutta kamina', 'kutte ki aulad', 'kutte ki jat', 'kuttiya', 'loda', 'lodu', 'lund', 'lund choos', 'lund khajoor', 'lundtopi', 'lundure', 'maa ki chut', 'madar chod', 'mooh mein le', 'mutth', 'raand', 'randi', 'kutti', 'randi', 'tatte', 'bhosada', 'chut', 'harak', 'anal', 'anus', 'arse', 'ass', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'blow job', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'cunt', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'f u c k', 'fudgepacker', 'fudge packer', 'flange', 'Goddamn', 'God damn', 'hell', 'homo', 'jerk', 'jizz', 'knobend', 'knob end', 'labia', 'muff', 'nigger', 'nigga', 'penis', 'piss', 'poop', 'prick', 'pube', 'pussy', 'queer', 'scrotum', 'sex', 'shit', 's hit', 'sh1t', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore', 'bisi', 'lode', 'Bcmc', 'lovde', 'chutiya', 'chutiye', 'madherchod', 'benchod', 'bcmc', 'madarchod', 'madrchod', 'madrchd', 'bhenchod', 'gandu', 'lund', 'lunn', 'lun', 'hutiya', 'chutchoot', 'chumtiya', 'chuntia', 'chutia', 'fucker', 'sucker', 'dickhead', 'asshole', 'niga', 'Niga', 'Nigga', '%bc%', 'gai', 'gea']

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
			channel = self.bot.get_channel(893049235241574430)
			messageContent = message.content.lower()
			messageContent = messageContent.split(" ")
			if len(messageContent) > 0:
				for word in messageContent:
					if word in bad_word:
						embed = discord.Embed(title=message.author.name, description=f"**Message**: {message.content}\n**Channel**: {message.channel.mention}\n**Banned**: {word}",color=0x2f3136)
						embed.timestamp = datetime.datetime.now()
						embed.set_footer(text=f"ID: {message.id}",icon_url=message.author.avatar_url)
						embed.set_thumbnail(url=message.author.avatar_url)
						return await channel.send(embed=embed)


def setup(bot):
	bot.add_cog(profanity(bot))