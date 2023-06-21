import discord
import asyncio
from discord.ext import commands,tasks
import datetime
import time 
import json
import random
from discord.ui import Button, View
import os 

class gwtask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Colour.blurple()
        self.giveaway_task.start()

    def cog_unload(self):
        self.giveaway_task.cancel()

    @tasks.loop(seconds=5)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        users = []
        with open(f"giveaways.json", "r") as f:
            giveaways = json.load(f)

        if len(giveaways) == 0:
            return

        for giveaway in giveaways:
            data = giveaways[giveaway]
            if int(time.time()) > data["end_time"] and not data["ended"]:
                channel = self.bot.get_channel(data["channel_id"])
               # ctx = data["ctx"]
                giveaway_message = await channel.fetch_message(int(giveaway))
                with open(f"giveaway_users/{data['button_id']}.txt", "r") as file:
                    for line in file:
                        stripped_line = line.strip()
                        users.append(stripped_line)

                if len(users) < data["winners"]:
                    winners_number = len(users)
                else:
                    winners_number = data["winners"]

                winners = random.sample(users, winners_number)
                prize = data["prize"]
                link = data["link"]
                host = data["host"]
                btn = Button(label=f'{len(users)} Entries', style=discord.ButtonStyle.grey)
                btn.disabled = True
                msg = ''
                for i in winners:
                  if len(winners) == 1:
                    msg += f'<@{i}>'
                  else:
                    msg += f'<@{i}>\n'

                result_embed2 = discord.Embed(
                    title="<:giveaway:1090322276748111982> {} ".format(data["prize"]),
                    color=0x030404,
                    description=f"Winner: {msg}\nHosted By: <@{host}>"
                )
                result_embed2.set_footer(icon_url=self.bot.user.display_avatar.url, text="Lock N Loaded | Giveaway Ended" if len(winners) == 1 else "Lock N Loaded | Giveaway Ended")
                result_embed2.timestamp = discord.utils.utcnow()
                result_embed = discord.Embed(color=0x2f3136,
                    description=f"You won [{prize}]({link})! Kindly contact the Giveaway Host <@{host}> to claim the Giveaway Prize!"
                                            )
                result_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text=f"Lock N Loaded | Giveaway Ended")
                #result_embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                await channel.send(content=f"{msg}", embed=result_embed, view=None)
                view = View()
                view.add_item(btn)
                await giveaway_message.edit(content=f"<a:Giveaways:1101739611295842344> **GIVEAWAY ENDED** <a:Giveaway:1101739437060259840>", embed=result_embed2, view=view)

                with open(f"giveaways.json", "r") as file:
                    json_data = json.load(file)
                    dara = {
                "prize": data["prize"],
                "host": data['host'],
                "winners": data["winners"],
                "end_time": data["end_time"],
                "channel_id": data["channel_id"],
                "button_id": data["button_id"],
                "link": data["link"], 
                "ended": True
            }
                    json_data[giveaway] = dara
                    #del json_data[giveaway]
                '''if os.path.exists(f"giveaway_users/{data['button_id']}.txt"):
                    os.remove(f"giveaway_users/{data['button_id']}.txt")
                else:
                    pass'''

                with open(f"giveaways.json", "w") as file:
                    json.dump(json_data, file, indent=4)