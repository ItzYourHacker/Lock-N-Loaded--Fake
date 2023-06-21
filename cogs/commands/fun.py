############MODULES#############
import discord
import requests
import aiohttp
import datetime
import random
from discord.ext import commands
from random import randint
from utils.Tools import *
from core import Cog, Ventura, Context
#14
#snipe | editsnipe | tickle | kiss | hug | slap | pat | feed | pet | howgay | slots | penis | meme | cat

from pathlib import Path
import json

PICKUP_LINES = json.loads(Path("pikup.json").read_text("utf8"))


def RandomColor():
    randcolor = discord.Color(random.randint(0x50101, 0x50101))
    return randcolor


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason="Lock N Loaded | Role Added ")

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason="Lock N Loaded | Role Removed")

    @blacklist_check()
    @ignore_check()
    @commands.command(name="tickle",
                      help="Tickle mentioned user .",
                      usage="Tickle <member>")
    async def tickle(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/tickle")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} tickle {user.mention}",
                color=0x50101)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @blacklist_check()
    @ignore_check()
    @commands.command(name="kiss",
                      help="Kiss mentioned user .",
                      usage="Kiss <member>")
    async def kiss(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/kiss")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} kisses {user.mention}",
                color=0x50101)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(usage="hug <member>")
    @blacklist_check()
    @ignore_check()
    async def hug(self, ctx, user: discord.Member = None):
        """Hug someone (or yourself)."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                res = await r.json()
                imgUrl = res["link"]
        embed = discord.Embed(
            title=
            f'{ctx.author.name} hugs {f"themselves. 😔" if user is None else f"{user.name} <a:KEKW_bruh:1072834782477688832>"}',
            color=0x50101,
        ).set_image(url=imgUrl)
        await ctx.send(embed=embed)

    @commands.command(name="slap",
                      help="Slap mentioned user .",
                      usage="Slap <member>")
    @blacklist_check()
    @ignore_check()
    async def slap(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/slap")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                color=0x50101,
                description=f"{ctx.author.mention} slapped {user.mention}",
            )
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="pat",
                      help="Pat mentioned user .",
                      usage="Pat <member>")
    @blacklist_check()
    @ignore_check()
    async def pat(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://some-random-api.ml/animu/pat")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} pats {user.mention}",
                color=0x50101)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="feed",
                      help="Feed mentioned user .",
                      usage="Feed <member>")
    @blacklist_check()
    @ignore_check()
    async def feed(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/feed")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} feeds {user.mention}",
                color=0x50101)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="pet", usage="Pet <member>")
    @blacklist_check()
    @ignore_check()
    async def pet(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("")
        else:
            r = requests.get("https://nekos.life/api/v2/img/pat")
            res = r.json()
            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                description=f"{ctx.author.mention} pets {user.mention}",
                color=0x50101)
            embed.set_image(url=res['url'])
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)

    @commands.command(name="howgay",
                      aliases=['gay'],
                      help="check someone gay percentage",
                      usage="Howgay <person>")
    @blacklist_check()
    @ignore_check()
    async def howgay(self, ctx, *, person):
        embed = discord.Embed(color=0x50101)
        responses = [
            '50', '75', '25', '1', '3', '5', '10', '65', '60', '85', '30',
            '40', '45', '80', '100', '150', '1000'
        ]
        embed.description = f'**{person} is {random.choice(responses)}% Gay** :rainbow:'
        embed.set_footer(text=f'How gay are you? - {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command(name="slots")
    @blacklist_check()
    @ignore_check()
    async def slots(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        slotmachine = f"[ {a} {b} {c} ]\n{ctx.author.mention}"
        if (a == b == c):
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} All Matching! You Won!",
                color=0x50101))
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} 2 Matching! You Won!",
                color=0x50101))
        else:
            await ctx.send(embed=discord.Embed(
                title="Slot machine",
                description=f"{slotmachine} No Matches! You Lost!",
                color=0x50101))

    @commands.command(name="penis",
                      aliases=['dick'],
                      help="Check someone`s dick`s size .",
                      usage="Dick [member]")
    @blacklist_check()
    @ignore_check()
    async def penis(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        size = random.randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        em = discord.Embed(title=f"**{user}'s** Dick size",
                           description=f"8{dong}D",
                           color=0x50101)
        em.set_footer(text=f'whats {user} dick size?')
        await ctx.send(embed=em)

    @commands.command(name="meme", help="give you a meme", usage="meme")
    @blacklist_check()
    @ignore_check()
    async def meme(self, ctx):
        embed = discord.Embed(title="""Take some memes""", color=0x50101)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/dankmemes/new.json?sort=hot'
            ) as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(
                    0, 25)]['data']['url'])
                embed.set_footer(text=f'Random Meme:')
                #embed.set_footer(text=f'Random Meme:')
                await ctx.send(embed=embed)

    @commands.command(name="cat", usage="cat")
    @blacklist_check()
    @ignore_check()
    async def cat(self, ctx):
        embed = discord.Embed(title="""Here's a cat""", color=0x50101)
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                res = await r.json()
                embed.set_image(url=res['file'])
                embed.set_footer(text=f'Random Cats:')
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="iplookup",
                             aliases=['ip', 'ipl'],
                             help="shows info about an ip",
                             usage="Iplookup [ip]")
    @blacklist_check()
    @ignore_check()
    async def iplookup(self, ctx, *, ip):
        async with aiohttp.ClientSession() as a:
            async with a.get(f"http://ipwhois.app/json/{ip}") as b:
                c = await b.json()
                try:
                    coordj = ''.join(f"{c['latitude']}" + ", " +
                                     f"{c['longitude']}")
                    embed = discord.Embed(
                        title="IP: {}".format(ip),
                        description=
                        f"```txt\n\nLocation Info:\nIP: {ip}\nIP Type: {c['type']}\nCountry, Country code: {c['country']} ({c['country_code']})\nPhone Number Prefix: {c['country_phone']}\nRegion: {c['region']}\nCity: {c['city']}\nCapital: {c['country_capital']}\nLatitude: {c['latitude']}\nLongitude: {c['longitude']}\nLat/Long: {coordj} \n\nTimezone Info:\nTimezone: {c['timezone']}\nTimezone Name: {c['timezone_name']}\nTimezone (GMT): {c['timezone_gmt']}\nTimezone (GMT) offset: {c['timezone_gmtOffset']}\n\nContractor/Hosting Info:\nASN: {c['asn']}\nISP: {c['isp']}\nORG: {c['org']}\n\nCurrency:\nCurrency type: {c['currency']}\nCurrency Code: {c['currency_code']}\nCurrency Symbol: {c['currency_symbol']}\nCurrency rates: {c['currency_rates']}\nCurrency type (plural): {c['currency_plural']}```",
                        color=0x50101)
                    embed.set_footer(
                        text='Thanks For Using Lock N Loaded',
                        icon_url=
                        "https://cdn.discordapp.com/avatars/1072443168471130132/0986983e3dc23d9d776362a929ec77dd.jpg"
                    )
                    await ctx.send(embed=embed)
                except KeyError:
                    embed = discord.Embed(
                        description=
                        "KeyError has occured, perhaps this is a bogon IP address, or invalid IP address?",
                        color=0x50101)
                    await ctx.send(embed=embed)


############################

    @commands.command(name="owner",
                      description="Gives the owner role to the user .",
                      aliases=['own'],
                      help="Gives the owner role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give owner")
    async def _owner(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['owner']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["owner"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Owner role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="coowner",
                      description="Gives the owner role to the user .",
                      aliases=['coown'],
                      help="Gives the owner role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give co owner")
    async def _coowner(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['coown']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["coown"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Co Owner role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="headadmin",
                      description="Gives the head admin role to the user .",
                      aliases=['hadmin'],
                      help="Gives the head admin role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give head admin")
    async def _headadmin(self, context: Context,
                         member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['headadmin']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["headadmin"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Head Admin role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="admin",
                      description="Gives the admin role to the user .",
                      help="Gives the admin role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give admin")
    async def _admin(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['admin']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["admin"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Admin role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="girladmin",
                      description="Gives the admin role to the user .",
                      aliases=['gadmin'],
                      help="Gives the admin role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    # @app_commands.describe(member="member to give girl admin")
    async def _girladmin(self, context: Context,
                         member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['gadmin']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["gadmin"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Girl Admin role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="headmod",
                      description="Gives the head mod role to the user .",
                      aliases=['hmod'],
                      help="Gives the head mod role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give head mod")
    async def _headmod(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['headmod']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["headmod"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Head Mod role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="mod",
                      description="Gives the mod role to the user .",
                      help="Gives the mod role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give mod")
    async def _mod(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['mod']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["mod"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Mod role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command(name="girlmod",
                      description="Gives the girl mod role to the user .",
                      aliases=['gmod'],
                      help="Gives the girl mod role to the user .")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    #@app_commands.describe(member="member to give girl mod")
    async def _girlmod(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
            role = data['gmod']
            await self.add_role(role=role, member=member)
            hacker = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Given <@&{role}> To {member.mention}",
                color=0x50101)
            hacker.set_author(name=f"{context.author}",
                              icon_url=f"{context.author.avatar}")
            hacker.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker)
        elif data["gmod"] == None:
            hacker1 = discord.Embed(
                description=
                f"❗ | Girl Mod role is not setuped in {context.guild.name}",
                color=0x50101)
            hacker1.set_author(name=f"{context.author}",
                               icon_url=f"{context.author.avatar}")
            hacker1.set_thumbnail(url=f"{context.author.avatar}")
            await context.send(embed=hacker1)

    @commands.command()
    async def pickupline(self, ctx: Context) -> None:
        """
        Gives you a random pickup line.
        Note that most of them are very cheesy.
        """
        random_line = random.choice(PICKUP_LINES["lines"])
        embed = discord.Embed(
            title=":cheese: Your pickup line :cheese:",
            description=random_line["line"],
            color=ctx.author.color,
        )
        embed.set_thumbnail(
            url=random_line.get("image", PICKUP_LINES["placeholder"]))
        await ctx.send(embed=embed)