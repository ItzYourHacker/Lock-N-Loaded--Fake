import discord
from core import Ventura, Cog
from discord.ext import commands
from utils.Tools import add_user_to_blacklist, getConfig

class AutoBlacklist(Cog):
    def __init__(self, client: Ventura):
      self.client = client
      self.spam_cd_mapping = commands.CooldownMapping.from_cooldown(5, 5, commands.BucketType.member)
      self.spam_command_mapping = commands.CooldownMapping.from_cooldown(6, 10, commands.BucketType.member)



    @commands.Cog.listener()
    async def on_message(self, message):
      bucket = self.spam_cd_mapping.get_bucket(message)
      ventura = '<@1072443168471130132>'
      retry = bucket.update_rate_limit()

      if retry:
        if message.content == ventura or message.content == "<@!1072443168471130132>":
          add_user_to_blacklist(message.author.id)
          embed = discord.Embed(description="**Successfully Blacklisted {} For Spam Mentioning Me!**".format(message.author.mention),color=0x50101)
          embed.set_thumbnail( url=self.client.user.display_avatar.url)
          await message.channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_command(self, ctx):
      bucket = self.spam_command_mapping.get_bucket(ctx.message)
      retry = bucket.update_rate_limit()
      if retry:
        add_user_to_blacklist(ctx.author.id)
        embed = discord.Embed(description="**Successfully Blacklisted {} For Spamming My Commands!**".format(ctx.author.mention),color=0x50101)
        embed.set_thumbnail( url=self.client.user.display_avatar.url)
        await ctx.reply(embed=embed)