import discord
from discord.utils import *
import aiohttp
from core import Ventura, Cog
import json
from utils.Tools import *
from discord.ext import commands



headers = {'Authorization': f'Bot MTA0NjM2MzI1NjAzOTY3ODAxMw.GHFfdu.etfXsJvL3rqrd2n_AeRCa_aqQFQ3nD3gar7XIc'}

class autorole(Cog):
    def __init__(self, bot: Ventura):
        self.bot = bot



    @Cog.listener()
    async def on_member_join(self, member):
        data = getDB(member.guild.id)
        arb = data["autorole"]["bots"]
        arh = data["autorole"]["humans"]
        if arb == []:
            return
        else:
            if member.bot != True:
                return
            elif member.bot:
                async with aiohttp.ClientSession(headers=headers, connector=None) as session:
                    for role in arb:
                        try:
                            async with session.put(f"https://discord.com/api/v10/guilds/{member.guild.id}/members/{member.id}/roles/{int(role)}", json={'reason': "Ventura | Auto Role"}) as req:
                                print(req.status)
                        except:
                            pass



    @Cog.listener()
    async def on_member_join(self, member):
        data = getDB(member.guild.id)
        arb = data["autorole"]["bots"]
        arh = data["autorole"]["humans"]
        if arh == []:
            return
        else:
            if member.bot:
                return
            elif member.bot != True:
                async with aiohttp.ClientSession(headers=headers, connector=None) as session:
                    for role in arh:
                        try:
                            async with session.put(f"https://discord.com/api/v10/guilds/{member.guild.id}/members/{member.id}/roles/{int(role)}", json={'reason': "Ventura | Auto Role"}) as req:
                                print(req.status)
                        except:
                            pass
