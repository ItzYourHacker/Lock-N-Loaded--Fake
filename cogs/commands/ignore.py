from __future__ import annotations
import discord
from discord.ext import commands, tasks
from core import *
from utils.Tools import *


class Ignore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="ignore", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def _ignore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_ignore.group(name="channel",
                   aliases=["chnl"],
                   invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _channel(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_channel.command(name="add")
    @commands.has_permissions(administrator=True)
    async def channel_add(self, ctx: Context, channel: discord.TextChannel):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            with open('ignore.json', 'r') as ignore:
                ignores = json.load(ignore)
                if str(channel.id) in ignores["ids"]:
                    embed = discord.Embed(
                        title="Error!",
                        description=
                        f"{channel.mention} is already in ignore channel list .",
                        color=0x50101)
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    add_channel_to_ignore(channel.id)
                    embed = discord.Embed(
                        description=
                        f"Now onwards {channel.mention} will be ignored by the bot.",
                        color=0x50101)
                    await ctx.reply(embed=embed, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5)

    @_channel.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def channel_remove(self, ctx, channel: discord.TextChannel):
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            remove_channel_from_ignore(channel.id)
            embed = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | {channel.mention} has been successfully removed from ignore channel list",
                color=0x50101)

            await ctx.reply(embed=embed, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5)
