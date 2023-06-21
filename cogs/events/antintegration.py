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
from core import Ventura, Cog
import time
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

class antintegration(Cog):
    def __init__(self, client: Ventura):
        self.client = client      
        self.headers = {"Authorization": f"Bot MTA0NjM2MzI1NjAzOTY3ODAxMw.GHFfdu.etfXsJvL3rqrd2n_AeRCa_aqQFQ3nD3gar7XIc"}
        print("Cog Loaded: Antintegration")
    @commands.Cog.listener()
    async def on_webhook_update(self, guild):
        try:
          data = getConfig(guild.id)
          anti = getanti(guild.id)
          punishment = data["punishment"]
          wled = data["whitelisted"]
          reason = "Creating Integration | Not Whitelisted"
          async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=30)):
            user = entry.user.id
            api = random.randint(8,9)
            if entry.user.id == 1060842035671732234:
              return
            elif entry.user == guild.owner:
              pass
            elif str(entry.user.id) in wled or anti == "off":
              pass
            else:
              if entry.action == discord.AuditLogAction.integration_create:
               async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                  took = round((datetime.now().timestamp() - start), 3)
                  log = await r.text()
                  if r.status in (200, 201, 204):
                            	logging.info("Successfully banned %s" % (user))
        except Exception as error:
            logging.error(error)