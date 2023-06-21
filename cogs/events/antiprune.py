import os
import discord
from discord.ext import commands
import requests
import sys
import setuptools
from itertools import cycle
import threading
import datetime
import logging
import time
from core import Ventura, Cog
import asyncio
import aiohttp
import tasksio
from discord.ext import tasks
import random
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies={"http": 'http://' + next(proxs)}

class antiprune(Cog):
    def __init__(self, client: Ventura):
        self.client = client      
        self.headers = {"Authorization": f"Bot MTA0NjM2MzI1NjAzOTY3ODAxMw.GHFfdu.etfXsJvL3rqrd2n_AeRCa_aqQFQ3nD3gar7XIc"}
        print("Cog Loaded: Antiprune")
    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        try:
            data = getConfig(member.guild.id)
            anti = getanti(member.guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            guild = member.guild
            reason = "Pruned Guild | Not Whitelisted"
            async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=30)):
              
              user = entry.user.id
              api = random.randint(8,9)
              if str(entry.user.id) in wled or anti == "off":
                if entry.action == discord.AuditLogAction.member_prune:
                  async with aiohttp.ClientSession(headers=self.headers) as session:
                    if punishment == "ban":
                      async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                        if r.status in (200, 201, 204):
                          logging.info("Successfully banned %s" % (user))
                    elif punishment == "kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r2:
                             if r2.status in (200, 201, 204):
                               logging.info("Successfully kicked %s" % (user))
                    elif punishment == "none":
                      mem = guild.get_member(entry.user.id)
                      await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)


                    else:
                       return
        except Exception as error:
            if isinstance(error, discord.Forbidden):
              return 