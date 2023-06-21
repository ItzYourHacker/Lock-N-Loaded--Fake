import json
from discord.ext import commands
import aiohttp, time
from core import Ventura, Cog
import asyncio



class antivanity(Cog):
    def __init__(self, client: Ventura):
        self.client = client
        self.headers = {"Authorization": f"Bot MTA2MDg0MjAzNTY3MTczMjIzNA.GYUmdt.cVARipSHnwzNpdokdWJ9FY_hWTlWdmsmCNCHwY"}
        print("Cog Loaded: AntiVanity")

    async def protect_vanity(self, guildid):
      start = time.perf_counter()
      with open('vanity.json') as idk:
        code = json.load(idk)
        if code[str(guildid)] != "":
          async with aiohttp.ClientSession(headers=self.headers) as session:
            jsonn = {"code": code[str(guildid)]}
            async with session.patch(f"https://ptb.discord.com/api/v10/guilds/{guildid}/vanity-url", json=jsonn) as response:
              end = time.perf_counter()
              print(f"{end - start} | {response.status}")
        else:
          return

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
      with open('vanity.json') as idk:
        code = json.load(idk)
        if before.vanity_url_code != after.vanity_url_code:
          asyncio.gather(*[self.protect_vanity(after.id)])
        else:
          return