import discord
import json
from discord.ext import commands

class Media(commands.Cog):
    def __init__(self, client):
        self.client = client
    def help_custom(self):
		      emoji = '<:media:1084325986448965653>'
		      label = "Media"
		      description = "Show You Media Commands"
		      return emoji, label, description

  
    @commands.Cog.listener()
    async def on_ready(self):
      with open("media.json", "r") as f:
        ok = json.load(f)
      for guild in self.client.guilds:
        if not str(guild.id) in ok:
          ok[str(guild.id)] = {"channel": []}
      with open("media.json", "w") as f:
        json.dump(ok,f,indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
      with open("media.json", "r") as f:
        ok = json.load(f)
      for guild in self.client.guilds:
        if not str(guild.id) in ok:
          ok[str(guild.id)] = {"channel": []}
      with open("media.json", "w") as f:
        json.dump(ok,f,indent=4)
    @commands.hybrid_group(invoke_without_command = True)
    async def media(self, ctx):
        prefix = ctx.prefix
        em = discord.Embed(
          title=f"Media Commands",
          description=f"`{prefix}media`\nConfigures the media only channels!\n\n`{prefix}media setup`\nSetups media only channels in the server.\n\n`{prefix}media remove`\nRemoves the media only channels in the server.\n\n`{prefix}media config`\nShows the configured media only channels for the server.\n\n`{prefix}media reset`\nRemoves all the channels from media only channels for the server.", color=0x0c0606)
        em.set_footer(text="Thanks for Choosing Lock N Loaded", icon_url=self.client.user.avatar)
        await ctx.send(embed=em)
          
    @media.command(name="setup", description="Setups media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def setup(self, ctx, *, channel: discord.TextChannel):
        with open("media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"].append(channel.id)

        with open("media.json", "w") as f:
            json.dump(media, f, indent = 4)

        await ctx.send(embed=discord.Embed(description=f"<:ventura_tick:1084496678406590464> | Successfully added {channel.mention} to my media database.", color=0x030404))


    @media.command(name="remove", description="Removes media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx, *, channel: discord.TextChannel):
        with open("media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"].remove(channel.id)

        with open("media.json", "w") as f:
            json.dump(media, f, indent = 4)

        await ctx.send(embed=discord.Embed(description=f"<:ventura_tick:1084496678406590464> | Successfully removed {channel.mention} from my media database.", color=0x030404))


    @media.command(name="config", aliases=["settings", "show"], description="Shows the configured media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def config(self, ctx):
        with open("media.json", "r") as f:
            media = json.load(f)
        
        chan = media[str(ctx.guild.id)]["channel"]

        channel = list([self.client.get_channel(id).mention for id in media[str(ctx.guild.id)]["channel"]])

        embed = discord.Embed(title = f"Media Only Channels for {ctx.guild.name}", color=0x0c0606)
        num = 0
        for i in channel:
            num += 1
            i = i.replace("['']", "")
            embed.add_field(name = f"{num}", value = i, inline = True)

        embed.set_footer(text = f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar)

        await ctx.send(embed = embed)


    @media.command(name="reset", description="Removes all the channels from media only channels for the server")
    @commands.has_permissions(administrator = True)
    async def reset(self, ctx):
        with open("media.json", "r") as f:
            media = json.load(f)

        media[str(ctx.guild.id)]["channel"] = []

        with open("media.json", "w") as f:
            json.dump(media, f, indent = 4)

        await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully cleared media database of this server.", color=0x030404))


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot != True:
            with open("media.json", "r") as f:
                media = json.load(f)

            channel = media[str(message.guild.id)]["channel"]

            if message.channel.id in channel:
                if message.attachments == []:
                    await message.delete()
                    await message.channel.send(f"This channel is configured for media only. You are only allowed to send media files.", delete_after = 1)