import discord
from discord.ext import commands
import os

from core import Cog, Ventura, Context
import discord_games as games
from utils.Tools import *
from discord_games import button_games as btn
import random
import asyncio
from utils.Tools import Timer


class Games(Cog):
    """Getting Bored? Dont worry, Games are here"""

    def __init__(self, client: Ventura):
        self.client = client

    @commands.hybrid_command(name="akinator",
                             help="Play akinator game with bot.",
                             aliases=["aki"],
                             usage="akinator")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _akinator(self, ctx: Context):
        game = btn.BetaAkinator()
        await game.start(ctx, timeout=None)

    @commands.hybrid_command(name="chess",
                             help="Play Chess Game with the bot.",
                             usage="Chess")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _chess(self, ctx: Context, player: discord.Member):
        if player == ctx.author:
            await ctx.send("You Cannot play game with yourself!",
                           mention_author=False)
        elif player.bot:
            await ctx.send("You cannot play with bots!")
        else:
            game = btn.BetaChess(white=ctx.author, black=player)
            await game.start(ctx)

    @commands.hybrid_command(name="hangman",
                             help="play hangman with bot.",
                             usage="Hangman")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _hangman(self, ctx: Context):
        game = games.Hangman()
        await game.start(ctx)

    @commands.hybrid_command(name="typerace",
                             help="check who is fast in typing",
                             aliases=["tr", "typeracer"],
                             usage="Typerace")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _typerace(self, ctx: Context):
        game = games.TypeRacer()
        await game.start(ctx, timeout=60)

    @commands.hybrid_command(name="rps",
                             help="Play Rock Paper Scissors with bot.",
                             aliases=["rockpaperscissors"],
                             usage="Rockpaperscissors")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _rps(self, ctx: Context, player: discord.Member = None):
        game = btn.BetaRockPaperScissors(player)
        await game.start(ctx, timeout=120)

    @commands.hybrid_command(name="tic-tac-toe",
                             help="play tic-tac-toe game",
                             aliases=["ttt", "tictactoe"],
                             usage="Ticktactoe <member>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(5, per=commands.BucketType.user, wait=False)
    @commands.guild_only()
    async def _ttt(self, ctx: Context, player: discord.Member):
        if player == ctx.author:
            await ctx.send("You Cannot play game with yourself!",
                           mention_author=False)
        elif player.bot:
            await ctx.send("You cannot play with bots!")
        else:
            game = btn.BetaTictactoe(cross=ctx.author, circle=player)
            await game.start(ctx, timeout=30)

    @commands.hybrid_command(name="wordle",
                             help="Wordle Game | Play with bot.",
                             usage="Wordle")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _wordle(self, ctx: Context):
        game = games.Wordle()
        await game.start(ctx, timeout=120)

    @commands.hybrid_command(name="2048",
                             help="Play 2048 game with bot.",
                             aliases=["twenty48"],
                             usage="2048")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _2048(self, ctx: Context):
        game = btn.BetaTwenty48()
        await game.start(ctx, win_at=2048)

    @commands.hybrid_command(name="memory-game",
                             help="How strong is your memory?",
                             aliases=["memory"],
                             usage="memory-game")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _memory(self, ctx: Context):
        game = btn.MemoryGame()
        await game.start(ctx)

    @commands.hybrid_command(name="number-slider",
                             help="slide numbers with bot",
                             aliases=["slider"],
                             usage="slider")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _number_slider(self, ctx: Context):
        game = btn.NumberSlider()
        await game.start(ctx)

    @commands.hybrid_command(name="battleship",
                             help="Enjoy the fight between some battle ships",
                             aliases=["battle-ship"],
                             usage="battleship <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _battle(self, ctx: Context, player: discord.Member):
        game = btn.BetaBattleShip(player1=ctx.author, player2=player)
        await game.start(ctx)

    @commands.hybrid_command(name="country-guesser",
                             help="Guess name of the country",
                             aliases=["guess", "guesser", "countryguesser"],
                             usage="country-guesser")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _country(self, ctx: Context):
        game = games.CountryGuesser(is_flags=True, hints=2)
        await game.start(ctx)

    @commands.hybrid_command(name="reaction")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(3, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def reaction(self, ctx):
        """
      See how fast you can get the correct emoji.
      """
        emoji = ["🍪", "🎉", "🧋", "🍒", "🍑"]
        random_emoji = random.choice(emoji)
        random.shuffle(emoji)
        embed = discord.Embed(
            title="Reaction time",
            description="After 1-15 seconds I will reveal the emoji.",
            color=0x01f5b6)
        first = await ctx.send(embed=embed)
        for react in emoji:
            await first.add_reaction(react)
        await asyncio.sleep(2.5)
        embed.description = "Get ready!"
        await first.edit(embed=embed)
        await asyncio.sleep(random.randint(1, 15))
        embed.description = f"GET THE {random_emoji} EMOJI!"
        await first.edit(embed=embed)

        def check(reaction, user):
            return reaction.message.id == first.id and str(
                reaction.emoji) == random_emoji and user != self.bot.user

        try:
            with Timer() as timer:
                reaction, user = await self.bot.wait_for("reaction_add",
                                                         check=check,
                                                         timeout=15)
        except asyncio.TimeoutError:
            embed.description = "Timeout"
            await first.edit(embed=embed)
        else:
            if str(reaction.emoji) == random_emoji:
                gettime = timer.total_time * 1000
                total_second = f"**{gettime:.2f}ms**"
                if gettime > 1000:
                    gettime = gettime / 1000
                    total_second = f"**{gettime:.2f}s**"
                embed.description = f"{user.mention} got the {random_emoji} in {total_second}"
                return await first.edit(embed=embed)
