import os
import discord
from discord.ext import commands
import requests
import sys
import setuptools
from itertools import cycle
from collections import Counter
import threading
import datetime
import logging
from core import Ventura, Cog
import time
import asyncio
import aiohttp
import tasksio
from discord.ui import View, Button
import json
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

class antipinginv(Cog):
    def __init__(self, client: Ventura):
        self.client = client
        self.spam_control = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)
        print("Cog Loaded: Antipinginv")

    @commands.Cog.listener()
    async def on_message(self, message):
      button = Button(emoji="<:invite:1073159512049057832>",label="Invite", url =  "https://discord.com/oauth2/authorize?client_id=1046363256039678013&scope=bot+applications.commands&permissions=268823646")
      button1 = Button(emoji="<:SupportTeam:1073159959866511370>",label="Support", url = "https://discord.gg/SXxXbjVt3j")
      try:
       
        with open("blacklist.json", "r") as f:
          data2 = json.load(f)
          ventura = '<@1046363256039678013>'
          try:
            data = getConfig(message.guild.id)
            anti = getanti(message.guild.id)
            prefix = data["prefix"]
            wled = data["whitelisted"]
            punishment = data["punishment"]
          except Exception:
            pass
          guild = message.guild
          if message.mention_everyone:
            if str(message.author.id) in wled or anti == "off":
              pass
            else:
              if punishment == "ban":
                await message.guild.ban(message.author, reason="Mentioning Everyone | Not Whitelisted")
              elif punishment == "kick":
                await message.guild.kick(message.author, reason="Mentioning Everyone | Not Whitelisted")
              elif punishment == "none":
                return


          elif message.content == ventura or message.content == "<@!1046363256039678013>":
            if str(message.author.id) in data2["ids"]:
              embed = discord.Embed(title="<a:astroz_cross:1072464778313879634> Blacklisted", description="You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/SXxXbjVt3j)")
              await message.reply(embed=embed, mention_author=False)
            else:

              embed = discord.Embed(description=f"""\Hey, I'm **Lock N Loaded**

Please use the following command instead: `&help` and view module drop-down 

If you continue to have problems, consider asking for help [Clickme](https://discord.gg/lnl).""",color=0x50101) 
              embed.set_author(name="Lock N Loaded", icon_url=self.client.user.display_avatar.url)
              embed.set_thumbnail(url =self.client.user.display_avatar.url)
              if guild.icon is not None:
                  embed.set_footer(  text=guild.name, icon_url=guild.icon.url)
              view = View()
              view.add_item(button)
              view.add_item(button1)
              await message.reply(embed=embed, mention_author=False, view=view)
          else:
            return
      except Exception as error:
        if isinstance(error, discord.Forbidden):
              return