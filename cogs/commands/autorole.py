from __future__ import annotations
import discord
import asyncio
import os
import logging
from discord.ext import commands
from utils.Tools import *
from discord.ext.commands import Context
from discord import app_commands
import time
import datetime
import re
from typing import *
from time import strftime
from core import Cog, Ventura, Context
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=
    "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)


class Autorole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="autorole", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole.command(name="config")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _ar_config(self, ctx):
        if data := getDB(ctx.guild.id):
            hum = list(data["autorole"]["humans"])
            bo = list(data["autorole"]["bots"])

            fetched_humans: list = []
            fetched_bots: list = []

        if data["autorole"]["humans"] != []:
            for i in hum:
                role = ctx.guild.get_role(int(i))
                if role is not None:
                    fetched_humans.append(role)

        if data["autorole"]["bots"] != []:
            for i in bo:
                role = ctx.guild.get_role(int(i))
                if role is not None:
                    fetched_bots.append(role)

            hums = "\n".join(i.mention for i in fetched_humans)
            if not hums:
                hums = " Humans Autorole Not Set."

            bos = "\n".join(i.mention for i in fetched_bots)
            if not bos:
                bos = " Bots Autorole Not Set."

            emb = discord.Embed(
                color=0x50101,
                title=f"Autorole of - {ctx.guild.name}").add_field(
                    name="__Humans__", value=hums,
                    inline=False).add_field(name="__Bots__",
                                            value=bos,
                                            inline=False)

            await ctx.send(embed=emb)

    @_autorole.group(name="reset",
                     help="Clear autorole config for the server .")
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_reset.command(name="humans",
                             help="Clear autorole config for the server .")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_reset(self, ctx):
        data = getDB(ctx.guild.id)
        rl = data["autorole"]["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if rl == []:
                embed = discord.Embed(
                    description=
                    "<a:astroz_cross:1072464778313879634> | This server don't have any autoroles setupped .",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if rl != []:
                    data["autorole"]["humans"] = []
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | Succesfully cleared all human autoroles for {ctx.guild.name} .",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_autorole_reset.command(name="bots")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_reset(self, ctx):
        data = getDB(ctx.guild.id)
        rl = data["autorole"]["bots"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if rl == []:
                embed = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | This server don't have any autoroles setupped .",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if rl != []:
                    data["autorole"]["bots"] = []
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | Succesfully cleared all bot autoroles for this server .",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_autorole_reset.command(name="all")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset_all(self, ctx):
        data = getDB(ctx.guild.id)
        brl = data["autorole"]["bots"]
        hrl = data["autorole"]["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(brl) == 0 and len(hrl) == 0:
                embed = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | This server don't have any autoroles setupped .",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if hrl != []:
                    data["autorole"]["bots"] = []
                    data["autorole"]["humans"] = []
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | Succesfully cleared all autoroles for this server .",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_autorole.group(name="humans", help="Setup autoroles for human users.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_humans.command(name="add",
                              help="Add role to list of autorole humans users."
                              )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_add(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        rl = data["autorole"]["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 15:
                embed = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | You have reached maximum channel limit for autorole humans which is 15 .",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if str(role.id) in rl:
                    embed1 = discord.Embed(
                        description=
                        "<a:astroz_cross:1072464778313879634> | {} is already in human autoroles ."
                        .format(role.mention),
                        color=0x50101)
                    await ctx.send(embed=embed1)
                else:
                    rl.append(str(role.id))
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | {role.mention} has been added to human autoroles .",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_autorole_humans.command(
        name="remove", help="Remove a role from autoroles for human users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_remove(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        rl = data["autorole"]["humans"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 0:
                embed = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | This server dont have any autrole humans setupped yet .",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if str(role.id) not in rl:
                    embed1 = discord.Embed(
                        description="{} is not in human autoroles .".format(
                            role.mention),
                        color=0x50101)
                    await ctx.send(embed=embed1)
                else:
                    rl.remove(str(role.id))
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | {role.mention} has been removed from human autoroles .",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_autorole.group(name="bots", help="Setup autoroles for bots.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_bots.command(name="add",
                            help="Add role to list of autorole bot users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_add(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        rl = data["autorole"]["bots"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 5:
                embed = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | You have reached maximum role limit for autorole bots which is 5.",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if str(role.id) in rl:
                    embed1 = discord.Embed(
                        description=
                        "<a:astroz_cross:1072464778313879634> | {} is already in bot autoroles."
                        .format(role.mention),
                        color=0x50101)
                    await ctx.send(embed=embed1)
                else:
                    rl.append(str(role.id))
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | {role.mention} has been added to bot autoroles .",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_autorole_bots.command(name="remove",
                            help="Remove a role from autoroles for bot users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_remove(self, ctx, role: discord.Role):
        data = getDB(ctx.guild.id)
        rl = data["autorole"]["bots"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 0:
                embed = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | This server dont have any autrole humans setupped yet .",
                    color=0x50101)
                await ctx.send(embed=embed)
            else:
                if str(role.id) not in rl:
                    embed1 = discord.Embed(
                        description=
                        "<a:astroz_cross:1072464778313879634> | {} is not in bot autoroles."
                        .format(role.mention),
                        color=0x50101)
                    await ctx.send(embed=embed1)
                else:
                    rl.remove(str(role.id))
                    updateDB(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tick:1072492486674616460> | {role.mention} has been removed from bot autoroles.",
                        color=0x50101)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)
