import discord
from discord import client, user
from discord.ext import commands
import json
from typing import Optional, Union, List
import time
import aiohttp
from os import name
from discord.ext.commands.errors import BotMissingPermissions
import asyncio
import random
import pathlib


afk_path = "database/afk.json"

black1 = 0
black2 = 0
black3 = 0

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(embed=discord.Embed(description=f"Only **{self.user}** Can Use This Command. Use {self.ctx.prefix}**{self.ctx.command}** To Run This Command", color=self.ctx.author.color),ephemeral=False)
            return False
        return True

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=None)
        self.value = None

    @discord.ui.button(label="Yes", emoji="<a:success:1002155523640152124>", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        self.value = 'Yes'
        self.stop()

    @discord.ui.button(label="No", emoji="<a:cross:1002155530334249071>", custom_id='No', style=discord.ButtonStyle.danger)
    async def truth(self, interaction, button):
        self.value = 'No'
        self.stop()
        
class afk(commands.Cog):

    def __init__(self, client, *args, **kwargs):
        self.client = client

    async def cog_after_invoke(self, ctx):
      #if ctx.author.id == harshid:
        ctx.command.reset_cooldown(ctx)

    async def update_data(self, afk, user, guild_id):
        if not f'{user.id}' in afk:
            afk[f'{user.id}'] = {}
            afk[f'{user.id}']['AFK'] = 'False'
            if guild_id in afk[f'{user.id}']['guild']:
                afk[f'{user.id}']['guild'].remove(guild_id)
            afk[f'{user.id}']['reason'] = 'None'

    async def time_formatter(self, seconds: float):

        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + " days, ") if days else "") + \
            ((str(hours) + " hours, ") if hours else "") + \
            ((str(minutes) + " minutes, ") if minutes else "") + \
            ((str(seconds) + " seconds, ") if seconds else "")
        return tmp[:-2]

    @commands.Cog.listener()
    async def on_message(self, message):
      try:
        with open(afk_path, 'r') as f:
            afk = json.load(f)
        if message.mentions:
            for user_mention in message.mentions:
                if afk[f'{user_mention.id}']['AFK'] == 'True':
                    if message.guild.id not in afk[f'{user_mention.id}']['guild']:
                        return
                    if message.author.bot: 
                        return
                    reason = afk[f'{user_mention.id}']['reason']
                    ok = afk[f'{user_mention.id}']['time']
                    wl = discord.Embed(description=f'**{str(user_mention)}** went AFK <t:{ok}:R> : {reason}', color=0x0c0606)
                    await message.channel.send(embed=wl)
                    content=message.author.mention

                    meeeth = int(afk[f'{user_mention.id}']['mentions']) + 1
                    afk[f'{user_mention.id}']['mentions'] = meeeth

                    with open(afk_path, 'w') as f:
                        json.dump(afk, f)

                    embed = discord.Embed(description=f'You were Mentioned in **{message.guild.name}** by **{message.author.name}#{message.author.discriminator}**!', color=discord.Color.from_rgb(black1, black2, black3))
                    embed.add_field(name="Total mentions :", value=meeeth, inline=False)
                    embed.add_field(name="Contents:", value=message.content, inline=False)
                    embed.add_field(name="Jump Url:", value=f"[Jump To Message]({message.jump_url})", inline=False)

                    if afk[f'{user_mention.id}']['dm'] == 'False':
                        return
                    await user_mention.send(embed=embed)
                if afk[f'{message.author.id}']['AFK'] == 'True':
                    hhh = afk[f'{message.author.id}']['guild']
                    if message.guild.id not in hhh:
                        return

                    meth = int(time.time()) - int(afk[f'{message.author.id}']['time'])
                    been_afk_for = await self.time_formatter(meth)
                    mentionz = afk[f'{message.author.id}']['mentions']
                    afk[f'{message.author.id}']['AFK'] == 'False'
                    afk[f'{message.author.id}']['guild'].remove(message.guild.id)
                    afk[f'{message.author.id}']['reason'] == None
                    wlba = discord.Embed(description=f'Welcome Back {str(message.author.mention)}, You got `{mentionz}` Mentions while You were AFK, I removed your AFK. You were afk for `{been_afk_for}`', color=0x0c0606)
                    await message.channel.send(embed=wlba)
                    content=message.author.mention

                    with open(afk_path, 'w') as f:
                        json.dump(afk, f)
                    await message.author.edit(nick=f'{message.author.display_name[5:]}')
                    if afk[f'{user_mention.id}']['AFK'] == 'True':
                        if message.guild.id not in afk[f'{user_mention.id}']['guild']:
                            return
                        reason = afk[f'{user_mention.id}']['reason']
                        ok = afk[f'{user_mention.id}']['time']
                        wlt = discord.Embed(description=f'**{str(user_mention)}** went AFK <t:{ok}:R> : {reason}', color=0x0c0606)
                        await message.channel.send(embed=wlt)
                        content=message.author.mention

                        meeeth = int(afk[f'{user_mention.id}']['mentions']) + 1
                        afk[f'{user_mention.id}']['mentions'] = meeeth

                        with open(afk_path, 'w') as f:
                            json.dump(afk, f)

                        embed = discord.Embed(description=f'You were Mentioned in **{message.guild.name}** by **{message.author.name}#{message.author.discriminator}**!', color=discord.Color.from_rgb(black1, black2, black3))
                        embed.add_field(name="Total mentions :", value=meeeth, inline=False)
                        embed.add_field(name="Contents:", value=message.content, inline=False)
                        embed.add_field(name="Jump Url:", value=f"[Jump To Message]({message.jump_url})", inline=False)

                        if afk[f'{user_mention.id}']['dm'] == 'False':
                            return

                        await user_mention.send(embed=embed)

            if not message.author.bot:
                await self.update_data(afk, message.author, message.guild.id)

        if afk[f'{message.author.id}']['AFK'] == 'True':
            hhh = afk[f'{message.author.id}']['guild']
            if message.guild.id not in hhh:
                return

            meth = int(time.time()) - int(afk[f'{message.author.id}']['time'])
            been_afk_for = await self.time_formatter(meth)
            mentionz = afk[f'{message.author.id}']['mentions']
            afk[f'{message.author.id}']['AFK'] == 'False'
            afk[f'{message.author.id}']['guild'].remove(message.guild.id)
            afk[f'{message.author.id}']['reason'] == None
            wlbat = discord.Embed(description=f'Welcome Back {str(message.author.mention)}, You got `{mentionz}` Mentions while You were AFK, I removed your AFK. You were afk for `{been_afk_for}`', color=0x0c0606)
            await message.channel.send(embed=wlbat)
            content=message.author.mention

        with open(afk_path, 'w') as f:
            json.dump(afk, f)
      except KeyError:
          pass

    @commands.hybrid_command(description="Set afk of the user in the server")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def afk(self, ctx, *, reason=None):

        with open(afk_path, 'r') as f:
            afk = json.load(f)

        if not reason:
            reason = "I am afk"

        if 'discord.gg' in reason:
            emd = discord.Embed(description=f"You can't Advertise in Afk Reason", color=0x0c0606)
            return await ctx.send(embed=emd)

        if 'DISCORD.GG' in reason:
            emd = discord.Embed(description=f"You can't Advertise in Afk Reason", color=0x0c0606)
            return await ctx.send(embed=emd)
        
        if '.GG/' in reason:
            emd = discord.Embed(description=f"You can't Advertise in Afk Reason", color=0x0c0606)
            return await ctx.send(embed=emd)
        
        if 'GG/' in reason:
            emd = discord.Embed(description=f"You can't Advertise in Afk Reason", color=0x0c0606)
            return await ctx.send(embed=emd)
        
        if 'gg/' in reason:
            emd = discord.Embed(description=f"You can't Advertise in Afk Reason", color=0x0c0606)
            return await ctx.send(embed=emd)

        if '.gg/' in reason:
            eme = discord.Embed(description=f"You can't Advertise in Afk Reason", color=0x0c0606)
            return await ctx.send(embed=eme)

        view = OnOrOff(ctx)
        

        em = discord.Embed(description="BOT SHOULD DM YOU ON EVERY MENTION IN THE SERVER WHILE YOUR AFK ?", color=0x0c0606)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not f'{ctx.author.id}' in afk:
            afk[f'{ctx.author.id}'] = {}
        if not view.value:
            return await test.edit(content="Time Is Gone Bro `Time Out`...!", view=None)
        if view.value == 'Yes':
            afk[f'{ctx.author.id}']['dm'] = 'True'
        if view.value == 'No':
            afk[f'{ctx.author.id}']['dm'] = 'False'

        afk[f'{ctx.author.id}']['AFK'] = 'True'
        afk[f'{ctx.author.id}']['reason'] = f'{reason}'
        afk[f'{ctx.author.id}']['time'] = int(time.time())
        afk[f'{ctx.author.id}']['mentions'] = 0
        try:
            ok = afk[f'{ctx.author.id}']['guild']
            ok.append(ctx.guild.id)
            afk[f'{ctx.author.id}']['guild'] = ok
        except:
            afk[f'{ctx.author.id}']['guild'] = []
            afk[f'{ctx.author.id}']['guild'].append(ctx.guild.id)
        await test.delete()
        af = discord.Embed(description=f'{ctx.author.mention} Your AFK is now set to: {reason}', color=0x0c0606)
        await ctx.send(embed=af)
        content=ctx.message.author.mention

        with open(afk_path, 'w') as f:
            json.dump(afk, f)

