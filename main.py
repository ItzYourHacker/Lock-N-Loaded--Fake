import os
from core.Ventura import Ventura
import asyncio
import discord
import traceback
from discord.ext.commands import Context
from discord import Spotify




client = Ventura()
tree = client.tree

async def Ventura_stats():
    while True:
        servers = len(client.guilds)
        users = sum(g.member_count for g in client.guilds
                    if g.member_count != None)
        sv_ch = client.get_channel(1109097758943612936)
        users_ch = client.get_channel(1109097758943612936)
        await asyncio.sleep(3000)
        await sv_ch.edit(name="Servers ; {}".format(servers))
        await users_ch.edit(name="Users ; {}".format(users))


class Devansh(discord.ui.Modal, title='Embed Configuration'):
    tit = discord.ui.TextInput(
        label='Embed Title',
        placeholder='Embed title here',
    )

    description = discord.ui.TextInput(
        label='Embed Description',
        style=discord.TextStyle.long,
        placeholder='Embed description optional',
        required=False,
        max_length=400,
    )

    thumbnail = discord.ui.TextInput(
        label='Embed Thumbnail',
        placeholder='Embed thumbnail here optional',
        required=False,
    )

    img = discord.ui.TextInput(
        label='Embed Image',
        placeholder='Embed image here optional',
        required=False,
    )

    footer = discord.ui.TextInput(
        label='Embed footer',
        placeholder='Embed footer here optional',
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.tit.value,
                              description=self.description.value,
                              color=0x030404)
        if not self.thumbnail.value is None:
            embed.set_thumbnail(url=self.thumbnail.value)
        if not self.img.value is None:
            embed.set_image(url=self.img.value)
        if not self.footer.value is None:
            embed.set_footer(text=self.footer.value)
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction,
                       error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.',
                                                ephemeral=True)

        traceback.print_tb(error.__traceback__)


@tree.command(name="embed", description="Create A Embed Using Lock N Loaded")
async def _embed(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(Devansh())


########################################











@client.event
async def on_ready():
    print("Loaded & Online!")
    print(f"Logged in as: {client.user}")
    print(f"Connected to: {len(client.guilds)} guilds")
    print(f"Connected to: {len(client.users)} users")
    await client.loop.create_task(Ventura_stats())
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)


from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def home():
    return "lamao ded"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()


keep_alive()









@client.event
async def on_command_completion(context: Context) -> None:

    full_command_name = context.command.qualified_name
    split = full_command_name.split("\n")
    executed_command = str(split[0])
    hacker = client.get_channel(1092564499892019220)
    if context.guild is not None:
        try:
            embed = discord.Embed(color=0x50101)
            embed.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed.set_thumbnail(url=f"{context.author.avatar}")
            embed.add_field(
                name="<a:Arrow:1072467877539618838> Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed.add_field(
                name="<a:Arrow:1072467877539618838> Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="<a:Arrow:1072467877539618838> Command Executed In :",
                value=
                f"{context.guild.name}  | ID: [{context.guild.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name=
                "<a:Arrow:1072467877539618838> Command Executed In Channel :",
                value=
                f"{context.channel.name}  | ID: [{context.channel.id}](https://discord.com/channel/{context.channel.id})",
                inline=False)
            embed.set_footer(text="Powered By Lock N Loaded",
                             icon_url=client.user.display_avatar.url)
            await hacker.send(embed=embed)
        except:
            print('FINE')
    else:
        try:

            embed1 = discord.Embed(color=0x50101)
            embed1.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed1.set_thumbnail(url=f"{context.author.avatar}")
            embed1.add_field(
                name="<a:Arrow:1072467877539618838> Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed1.add_field(
                name="<a:Arrow:1072467877539618838> Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed1.set_footer(text="Powered By Lock N Loaded",
                              icon_url=client.user.display_avatar.url)
            await hacker.send(embed=embed1)
        except:
            print("FINE")


@client.command()
async def makeembed(ctx, *, description):
    if not description:
        await ctx.channel.send(
            "One or more values are missing. Command should look like 'makeEmbed (description)'"
        )

    embed = discord.Embed(description=description, color=0x50101)
    if ctx.guild.icon is not None:
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)

    await ctx.send(embed=embed)


@client.command()
async def spotify(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                luci = discord.Embed(
                    title = f"{user.name}'s Spotify",
                    description = "Listening to {}".format(activity.title),
                    color = 0x0c0606)
                luci.set_thumbnail(url=activity.album_cover_url)
                luci.add_field(name="Artist", value=activity.artist)
                luci.add_field(name="Album", value=activity.album)
                luci.set_footer(text="Song started at {}".format(
              activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=luci)
              

async def main():
    async with client:
        os.system("clear")
        await client.load_extension("cogs")
        await client.load_extension("jishaku")
        await client.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())