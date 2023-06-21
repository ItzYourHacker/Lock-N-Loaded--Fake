import discord
from discord.ext import commands
from core import Ventura, Cog
from discord.utils import *
from discord import *
from utils.Tools import *

from discord.utils import get
from utils.Tools import getDB




class Vcroles2(Cog):
    def __init__(self, bot: Ventura):
        self.bot = bot



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data = getDB(member.guild.id)
        if member.bot:
            if data["vcrole"]["bots"] == "":
                return
            else:
                if not before.channel and after.channel:
                    r = data["vcrole"]["bots"]
                    br = get(member.guild.roles, id=r)
                    await member.add_roles(br, reason="Ventura | VC Roles (Joined VC)")
                elif before.channel and not after.channel:
                    r1 = data["vcrole"]["bots"]
                    br1 = get(member.guild.roles, id=r1)
                    await member.remove_roles(br1, reason="Ventura | VC Roles (Left VC)")
        elif member.bot != True:
            if data["vcrole"]["humans"] == "":
                return
            else:
                if not before.channel and after.channel:
                    r2 = data["vcrole"]["humans"]
                    br2 = get(member.guild.roles, id=r2)
                    await member.add_roles(br2, reason="Ventura | VC Roles (Joined VC)")
                elif before.channel and not after.channel:
                    r3 = data["vcrole"]["humans"]
                    br3 = get(member.guild.roles, id=r3)
                    await member.remove_roles(br3, reason="Ventura | VC Roles (Left VC)")