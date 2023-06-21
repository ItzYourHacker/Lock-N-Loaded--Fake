import discord
import asyncio
from discord.ext import commands
import datetime
import time 
import json
import random
from discord.ui import View, Button
import aiohttp
from typing import Union

giveaway_users = []


def convert(date):
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    i = {"s": "Seconds", "m": "Minutes", "h": "Hours", "d": "Days"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])

    except ValueError:
        return -2

    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx

class test(BasicView):
    def __init__(self, ctx: commands.Context, time):
        super().__init__(ctx, timeout=time)
        self.value = None
    
    @discord.ui.button(label=f"0",emoji=f'🎉', style=discord.ButtonStyle.gray,custom_id=f'give')
    async def dare(self, interaction: discord.Interaction, button):
        pass
        '''giveaway_users = []
        try:
            with open(f"giveaway_users/{interaction.channel.name}.txt", "r") as file:
                for line in file:
                    stripped_line = line.strip()
                    giveaway_users.append(stripped_line)

            if str(interaction.user.id) not in giveaway_users:
                number = int(button.label) if button.label else 0
                button.label = str(number + 1)
                await interaction.response.edit_message(view=self)
                await interaction.channel.send(f"<@{interaction.user.id}> You have successfully entered the giveaway!", delete_after=1)
                a = interaction.user.id
                with open(f"giveaway_users/{interaction.channel.name}.txt", "a") as file:
                    file.write(f"{str(a)}\n")

            else:
                number = int(button.label)
                button.label = str(number - 1)
                await interaction.response.edit_message(view=self)
                await interaction.channel.send(f"<@{interaction.user.id}> You have successfully left the giveaway!", delete_after=1)
                #await interaction.response.send_message("Left Giveaway", ephemeral=True)
                a = interaction.user.id
                giveaway_users.remove(str(a))
                with open(f"giveaway_users/{interaction.channel.name}.txt", 'w') as file:
                    idk = file.read().split('\n').remove(str(a))
                file.write(f"{idk}")
                #await interaction.response.send_message("You Have Left This Giveaway", ephemeral=True)
        except IOError:
            if len(str(interaction.channel.name)) <= 4:
                await interaction.response.send_message(f"<a:astroz_cross:1072464778313879634> This Giveaway Has Been Ended.", ephemeral=True)'''


class give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x030404

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
      if interaction.type == discord.InteractionType.component:
        with open('giveaways.json', 'r') as f:
          data = json.load(f)
        if str(interaction.message.id) in data:
          button = interaction.message.components[0].children[0]
          giveaway_users = []
          try:
              with open(f"giveaway_users/{interaction.channel.name}.txt", "r") as file:
                for line in file:
                    stripped_line = line.strip()
                    giveaway_users.append(stripped_line)

              if str(interaction.user.id) not in giveaway_users:
                number = int(button.label) if button.label else 0
                btn = Button(label=str(number+1),emoji=f'🎉', style=discord.ButtonStyle.gray,custom_id=f'give')
                view = View()
                view.add_item(btn)
                await interaction.response.edit_message(view=view)
                
                a = interaction.user.id
                with open(f"giveaway_users/{interaction.channel.name}.txt", "a") as file:
                    file.write(f"{str(a)}\n")

              else:
                number = int(button.label)
                btn = Button(label=str(number-1),emoji=f'🎉', style=discord.ButtonStyle.gray,custom_id=f'give')
                view = View()
                view.add_item(btn)
                await interaction.response.edit_message(view=view)
                
                #await interaction.response.send_message("Left Giveaway", ephemeral=True)
                a = interaction.user.id
                giveaway_users.remove(str(a))
                with open(f"giveaway_users/{interaction.channel.name}.txt", 'w') as file:
                    idk = file.read().split('\n').remove(str(a))
                file.write(f"{idk}")
                #await interaction.response.send_message("You Have Left This Giveaway", ephemeral=True)
          except IOError:
            if len(str(interaction.channel.name)) <= 4:
                await interaction.response.send_message(f"<a:astroz_cross:1072464778313879634> This Giveaway Has Been Ended.", ephemeral=True)
        else:
          pass
      else:
        pass

    @commands.hybrid_command(description="Creates a giveaway")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def gstart(self, ctx):
        await ctx.message.delete()
        init = await ctx.send(embed=discord.Embed(
            title=f"<a:Giveaway:1101739437060259840> Giveaway <a:Giveaways:1101739611295842344>",
            description=f"<a:Giveaway:1101739437060259840> **Answer the questions for the giveaway.**",
            color=self.color)
                              .set_footer(icon_url=self.bot.user.display_avatar.url, text=self.bot.user.name))

        questions = [
            "**[1]** **Can You Tell Me What The Giveaway Prize Will Be ? \n Like : `1M OWO CASH`**",
            f"**[2]** **In Which Channel Would You Like The Giveaway Should Be Created ? ( Please Mention The Channel In Which The Giveaway Should Be Created )\n Example : {ctx.channel.mention}**",
            "**[3]** **Mention The Time of the Giveaway!  \n Example: `10d` | `10h` | `10m` | `10s`**",
            "**[4]** **Winners for the Giveaway!** ? \n **Example: `1` | `2` | `3`**"
        ]

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        index = 1
        answers = []
        now = int(time.time())
        question_message = None
        for question in questions:
            embed = discord.Embed(
                title=f"<a:Giveaway:1101739437060259840> Giveaway <a:Giveaways:1101739611295842344>",
                description=question,
                color=0x030404
            ).set_footer(icon_url=self.bot.user.display_avatar.url, text=f"Lock N Loaded | Giveaway")
            if index == 1:
                question_message = await ctx.send(embed=embed)
            else:
                await question_message.edit(embed=embed)

            try:
                user_response = await self.bot.wait_for(f"message", timeout=None, check=check)
                await user_response.delete()
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(
                    title=f"Error",
                    color=self.color,
                    description=f"<:ventura_tick:1084496678406590464> | Please setup the giveaway again ):."
                ))
                return
            else:
                answers.append(user_response.content)
                index += 1
        try:
            channel_id = int(answers[1][2:-1])
        except ValueError:
            await ctx.send("<a:astroz_cross:1072464778313879634> | Mention The Channel Correctly!, do it like {}.".format(ctx.channel.mention))
            return

        try:
            winners = abs(int(answers[3]))
            if winners == 0:
                await ctx.send(f"<a:astroz_cross:1072464778313879634> | You did not enter the number correctly.")
                return
        except ValueError:
            await ctx.send(f"<a:astroz_cross:1072464778313879634> | You did not enter an correctly.")
            return
        prize = answers[0].title()
        channel = self.bot.get_channel(channel_id)
        converted_time = convert(answers[2])
        if converted_time == -1:
            await ctx.send(f"<a:astroz_cross:1072464778313879634> | Enter The Time Correctly (s|m|d|h)")
        elif converted_time == -2:
            await ctx.send(f"<a:astroz_cross:1072464778313879634> | Enter The Time Correctly (s|m|d|h)")
            return
        await init.delete()
        await question_message.delete()
        giveaway_embed = discord.Embed(
            title="<a:Giveaway:1101739437060259840> {} ".format(prize),
            color=self.color,
            description=f'Ends: <t:{now + converted_time[0]}:R> (<t:{now + converted_time[0]}:f>)\n'
                        f'Hosted by: {ctx.author.mention}\n\n'
                        f'[Invite Lock N Loaded](https://discord.com/oauth2/authorize?client_id=1046363256039678013&scope=bot+applications.commands&permissions=268823646) 🔹 [Support Server](https://discord.gg/lnlhq)\n'
                        
        ) \
            .set_footer(icon_url=self.bot.user.display_avatar.url, text=f"{winners} Winner | Ends at") \
            #.set_thumbnail(url=self.bot.user.display_avatar.url)

        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time[0])
        action_row = test(ctx, now+converted_time[0])
        giveaway_message = await channel.send(content="<a:Giveaways:1101739611295842344> **GIVEAWAY STARTED** <a:Giveaway:1101739437060259840>", embed=giveaway_embed, view=action_row)
        with open(f"giveaways.json", "r") as f:
            giveaways = json.load(f)

            data = {
                "prize": prize,
                "host": ctx.author.id,
                "winners": winners,
                "end_time": now + converted_time[0],
                "channel_id": channel.id,
                "button_id": channel.name,
                "link": giveaway_message.jump_url,
                "ended": False
            }
            giveaways[str(giveaway_message.id)] = data

        with open(f"giveaways.json", "w") as f:
            json.dump(giveaways, f, indent=4)
        with open(f"giveaway_users/{data['button_id']}.txt", "w"):
            pass


    @commands.hybrid_command(description="Ends a giveaway early")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def gend(self, ctx, message: int):
      try:
        msg = await ctx.fetch_message(message)
      except:
        await ctx.send("Error")
      with open('giveaways.json', 'r') as f:
        data = json.load(f)
      if not str(message) in data:
        return await ctx.send("No ongoing giveaway found")
      data2 = {
                "prize": data[str(message)]["prize"],
                "host": data[str(message)]['host'],
                "winners": data[str(message)]["winners"],
                "end_time": int(time.time()),
                "channel_id": data[str(message)]["channel_id"],
                "button_id": data[str(message)]["button_id"],
                "link": data[str(message)]["link"], 
                "ended": False
            }
      data[str(message)] = data2
      with open(f"giveaways.json", "w") as f:
        json.dump(data, f, indent=4)


    @commands.hybrid_command(description="Reroll a giveaway")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def greroll(self, ctx, message: int):
      users = []
      try:
        msg = await ctx.fetch_message(message)
      except:
        await ctx.send("Error")
      with open('giveaways.json', 'r') as f:
        data = json.load(f)
      if str(message) not in data:
        return await ctx.send("No previous giveaway found with this message id")
      elif not data[str(message)]["ended"]:
        return await ctx.send("Giveaway is still going on")
      else:
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        await ctx.send("Winners do you want to reroll for the giveaway?\n\n**Note**: You must choose a number between 1 and 15.")
        try:
          user_response = await self.bot.wait_for(f"message", timeout=None, check=check)
          await user_response.delete()
        except asyncio.TimeoutError:
          await ctx.send(embed=discord.Embed(
                    title=f"Error",
                    color=self.color,
                    description=f"<:ventura_tick:1084496678406590464> | You took too long to answer this question, Please setup the giveaway again ):."
                ))
          return
        try:
          winners = int(user_response.content)
        except:
          await ctx.send("Invalid Winners, run command again!")
        if winners > 15 or winners < 1:
          return await ctx.send("Either winners are more than 15 or less than 1")
        with open(f"giveaway_users/{data[str(message)]['button_id']}.txt", "r") as file:
          for line in file:
            stripped_line = line.strip()
            users.append(stripped_line)
          if len(users) < winners:
            winners = len(users)
          msg = ''
          winner = random.sample(users, winners)
          for i in winner:
            if len(winner) == 1:
              msg += f'<@{i}>'
            else:
              msg += f'<@{i}>\n'
          prize = data[str(message)]["prize"]
          link = data[str(message)]["link"]
          host = data[str(message)]["host"]
          result_embed = discord.Embed(color=0x030404,
                    description=f"You won [{prize}]({link})! Kindly contact the Giveaway host <@{host}> to claim your rewards"
                                            )
          result_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text=f"Lock N Loaded | Giveaway Ended")
          #result_embed.set_thumbnail(url=self.bot.user.display_avatar.url)
          await ctx.channel.send(content=f"{msg}", embed=result_embed, view=None)