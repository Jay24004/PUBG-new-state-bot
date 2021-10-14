import asyncio
import dataclasses
import logging
import random
from itertools import islice
from string import Template
import datetime
import discord
from discord.ext import commands

from utils import Winner, TicTacToe, InvalidMove, PlayerStats
from utils.util import Pag

from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [814374218602512395, 829615142450495601, 888085276801531967]

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats = {}
        self.logger = logging.getLogger(__name__)

    def is_bot_channel():
        async def predicate(ctx):
            data = await ctx.bot.config.find(ctx.guild.id)
            if data is None: return await ctx.send("This is not a bot-channel or there is no bot channel in server", hidden=True)
            if data:
                return ctx.channel.id == data['bot_channel'] or ctx.channel.id in data['bot_channel']
            else:
                return False
        return commands.check(predicate)

    async def chunk_results(self, it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    async def display_board(self, messageable, game, *, content=None):
        board = game.board
        desc = f"""
        ```yaml
          1|2|3
        1|{board[0][0].to_piece()}|{board[0][1].to_piece()}|{board[0][2].to_piece()}
        2|{board[1][0].to_piece()}|{board[1][1].to_piece()}|{board[1][2].to_piece()}
        3|{board[2][0].to_piece()}|{board[2][1].to_piece()}|{board[2][2].to_piece()}
        ```
        """

        embed = discord.Embed(
            title=f"TicTacToe ({game.player_one.display_name} VS {game.player_two.display_name})",
            description=desc,
        )
        await messageable.edit(content=content, embed=embed)

    async def update_stats(self, member, end_state, was_player_one):
        player = await self.bot.tictactoe.find_by_custom({})

        if end_state.value == 1:
            if was_player_one:
                player.wins += 1
            else:
                player.losses += 1

        elif end_state.value == 2:
            if was_player_one:
                player.losses += 1
            else:
                player.wins += 1

        elif end_state.value == 3:
            player.draws += 1

        self.stats[member.id] = player

        data = dataclasses.asdict(player)
        data["_id"] = data.pop("player_id")
        await self.bot.tictactoe.upsert(data)

    async def populate_stats(self):
        # Handle on_ready being called multiple times
        if self.stats:
            return

        data = await self.bot.tictactoe.get_all()
        for document in data:
            player = PlayerStats(
                document["_id"],
                wins=document["wins"],
                losses=document["losses"],
                draws=document["draws"],
            )
            self.stats[document["_id"]] = player

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("I'm ready!")
        await self.populate_stats()

    @cog_ext.cog_slash(name="tictactoe", description="TicTacToe Games", options=[create_option(name="player", description="select player you want to play with", option_type=8, required=False)],guild_ids=guild_ids)
    @commands.max_concurrency(1, commands.BucketType.channel)
    #@is_bot_channel()
    async def tictactoe(self, ctx, player_two: discord.Member = None):
        def check(m):
            return m.channel == ctx.channel and m.author == current_player

        def react_check(payload):
            return (
                payload.message_id == difficulty_message.id
                and payload.user_id == ctx.author.id
                and str(payload.emoji) in ["1️⃣", "2⃣"]
            )

        is_bot = False
        difficulty = 1
        # Disable difficulty atm
        if not player_two or player_two == ctx.guild.me and False:
            player_two = ctx.guild.me
            is_bot = True

            embed = discord.Embed(
                title="Please pick a difficulty",
                description=":one: - Easy\n:two: - Hard",
            )

            difficulty_message = await ctx.send(embed=embed)
            await difficulty_message.add_reaction("1️⃣")
            await difficulty_message.add_reaction("2⃣")

            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add", check=react_check, timeout=25
                )
            except asyncio.TimeoutError:
                await ctx.send("I picked hard on your behalf :)")
            else:
                if str(payload.emoji) == "1️⃣":
                    difficulty = 2.5
                    await ctx.send("Set difficulty to easy", delete_after=10)
                else:
                    await ctx.send("Set difficulty to hard", delete_after=10)
            finally:
                await difficulty_message.delete()

        m = await ctx.send("Starting game!")

        game = TicTacToe(
            player_one=ctx.author,
            player_two=player_two,
            is_agaisnt_computer=is_bot,
            difficulty=difficulty,
        )

        player_one_start = random.choice([True, False])
        if not player_one_start:
            await game.flip_player()

        await self.display_board(m, game)

        while (winner := await game.is_over()) == Winner.NO_WINNER:
            current_player = ctx.author if game.is_player_one_move else player_two

            if not game.is_player_one_move and is_bot:
                await self.display_board(
                    m,
                    game,
                    content=f"{current_player.mention}, please pick where you wish to play in the format `row column`",
                )
                await game.ai_turn()
                await asyncio.sleep(random.randrange(0, 5))
                continue

            try:
                await self.display_board(
                    m,
                    game,
                    content=f"{current_player.mention}, please pick where you wish to play in the format `row column`",
                )
                msg = await self.bot.wait_for("message", check=check, timeout=25)
            except asyncio.TimeoutError:
                await game.flip_player()
                await ctx.send(f"{current_player.mention}, you missed your turn!")
            else:
                content = msg.content

                await msg.delete()

                if not len(content) == 3:
                    await ctx.send(
                        f"{current_player.mention}, Invalid move sequence, please see the format and try again",
                        delete_after=10,
                    )
                    continue

                row, column = content.split()
                try:
                    await game.make_move(row, column)
                except InvalidMove:
                    await ctx.send(
                        f"{current_player.mention}, illegal move sequence, please try again",
                        delete_after=10,
                    )
                    continue

        content = Template(str(winner)).safe_substitute(
            {"MENTIONONE": ctx.author.mention, "MENTIONTWO": player_two.mention}
        )
        await self.display_board(m, game, content=content)

        await self.update_stats(ctx.author, winner, True)
        await self.update_stats(player_two, winner, False)

    @cog_ext.cog_slash(name="score", description="show stats of player", guild_ids=guild_ids, options=[create_option(name="player", description="select player to see there stats", option_type=8, required=False)])
    #@is_bot_channel()
    async def score(self, ctx, player: discord.Member = None):
        """Returns your TicTacToe stats"""
        player = player or ctx.author
        data = await self.bot.tictactoe.find(player.id)
        if not data: return await ctx.send(f"I have no stats for `{player.display_name}`")

        embed = discord.Embed(
            title=f"TicTacToe stats for: `{player.display_name}`",
            description=f"Wins: **{data['wins']}**\n"
            f"Losses: **{data['losses']}**\n"
            f"Draws: **{data['draws']}**",
            timestamp=datetime.datetime.now(),
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="leaderboard", description="shows leaderboard of tictactoe game", guild_ids=guild_ids,options=[create_option(name="type", description="select filter for the leaderboard", 
        choices=[create_choice(
                name="Wins",
                value="aww"
                ),
            create_choice(
                name="Losses",
                value="losses"
                ),
            create_choice(
                name="Draws",
                value="draws"
                ),],option_type=3, required=False)])
    #@is_bot_channel()
    async def leaderboard(self, ctx, stat_type="wins"):
        """Shows the TicTacToe leaderboard"""
        if (stat_type := stat_type.lower()) not in ["wins", "losses", "draws"]:
            return await ctx.send("Invalid stat type requested!")

        data = await self.bot.tictactoe.get_all()
        if not data:
            return await ctx.send("I have no stats to show.")

        #data = sorted(data, key=lambda x: getattr(x, stat_type), reverse=True)
        data = sorted(data, key=lambda x: x[stat_type], reverse=True)
        #data = await self.chunk_results(data, 10)

        pages , i = [], 1
        for item in data:
            page = ""
            page += f"{i}.<@{item['_id']}> - {item[stat_type]}\n"
            pages.append(page)
            i += 1

        await Pag(
            title=f"TicTacToe leaderboard for `{stat_type}`",
            colour=0x11eca4,
            entries=pages,
            length=5,
        ).start(ctx)

def setup(bot):
    bot.add_cog(Games(bot))