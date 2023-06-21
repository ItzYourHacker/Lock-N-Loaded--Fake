import os
import discord
from discord.ext import commands
from utils.Tools import *
from core import Ventura, Cog
import requests
import sys
import setuptools
from itertools import cycle
import threading
import datetime
import logging
import time
import asyncio
import aiohttp
import tasksio
from discord.ext import tasks
import random

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies={"http": 'http://' + next(proxs)}

class antiban(Cog):
    def __init__(self, client: Ventura):
        self.client = client      
        self.headers = {"Authorization": f"Bot MTA0NjM2MzI1NjAzOTY3ODAxMw.GHFfdu.etfXsJvL3rqrd2n_AeRCa_aqQFQ3nD3gar7XIc"}
        print("Cog Loaded: AntiBan")
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user) -> None:
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            reason = "Banning Members | Not Whitelisted"
            api = random.randint(8,9)
            async for entry in guild.audit_logs(
                limit=1):
                  user = entry.user.id
                  if user == 1060842035671732234:
                    pass
                  elif entry.user == guild.owner or str(entry.user.id) in wled or anti == "off":
                    pass
                  else:
                    async with aiohttp.ClientSession(headers=self.headers) as session:
                     if entry.action == discord.AuditLogAction.ban:
                      if punishment == "ban":
                       async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                         await guild.unban(user=user, reason=reason)
                         if r.status in (200, 201, 204):
                           
                           logging.info("Successfully banned %s" % (user))
                      elif punishment == "kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r2:
                             await guild.unban(user=user, reason=reason)
                             if r2.status in (200, 201, 204):
                               
                               logging.info("Successfully kicked %s" % (user))
                      elif punishment == "none":
                       mem = guild.get_member(entry.user.id)
                       await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                       await guild.unban(user=user, reason=reason)
                     else:
                       return
        except Exception as error:
          if isinstance(error, discord.Forbidden):
              return
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User) -> None:
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            wled = data["whitelisted"]
            punishment = data["punishment"]
            reason = "Unbanning Members | Not Whitelisted"
            async for entry in guild.audit_logs(
                limit=1):
              use = entry.user.id
              api = random.randint(8,9)
              if entry.user.id == self.client.user.id or entry.user.id == guild.owner_id or str(entry.user.id) in wled or anti == "off":
               return
              async with aiohttp.ClientSession(headers=self.headers) as session:
                if entry.action == discord.AuditLogAction.unban:
                 if punishment == "ban":
                  async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, use), json={"reason": reason}) as r:
                    victim = await self.client.fetch_user(user.id)
                    await guild.ban(victim, reason=reason)
                    if r.status in (200, 201, 204):
                      
                      logging.info("Successfully banned %s" % (use))
                 elif punishment == "kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, use), json={"reason": reason}) as r2:
                           await guild.ban(discord.Object(int(user.id)), reason=reason)
                           if r2.status in (200, 201, 204):
                               
                               logging.info("Successfully kicked %s" % (use))
                 elif punishment == "none":
                  mem = guild.get_member(entry.user.id)
                  await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                  await guild.ban(victim, reason=reason)
                else:
                       return
        except Exception as error:
            logging.error(error)