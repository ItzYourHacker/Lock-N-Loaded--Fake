import discord
import wavelink
from wavelink.ext import spotify
from discord.ext import commands
import logging
from typing import Any, Dict, Union, Optional
from discord.enums import try_enum
import os
import datetime
import datetime as dt
import datetime

import typing as t
import requests
import re
from discord.ext.commands.errors import CheckFailure
import asyncio
import os
from wavelink import Player
import async_timeout
from utils.Tools import *

LYRICS_URL = "https://some-random-api.ml/lyrics?title="
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"


class NotConnectedToVoice(CheckFailure):
    """User not connected to any voice channel"""

    pass


class PlayerNotConnected(CheckFailure):
    """Player not connected"""

    pass


class MustBeSameChannel(CheckFailure):
    """Player and user not in same channel"""

    pass


class NothingIsPlaying(CheckFailure):
    """Nothing is playing"""

    pass


class NotEnoughSong(CheckFailure):
    """Not enough songs in queue"""

    pass


class InvalidLoopMode(CheckFailure):
    """Invalid loop mode"""

    pass


class DisPlayer(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = asyncio.Queue()
        self.bound_channel = None
        self.track_provider = "yt"

    async def destroy(self) -> None:
        self.queue = None

        await super().stop()
        await super().disconnect()

    async def do_next(self) -> None:
        if self.is_playing():
            return

        timeout = int(os.getenv("DISMUSIC_TIMEOUT", 300))

        try:
            with async_timeout.timeout(timeout):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            if not self.is_playing():
                await self.destroy()

            return

        self._source = track
        await self.play(track)
        self.client.dispatch("dismusic_track_start", self, track)
        await self.invoke_player()

    async def invoke_player(self, ctx: commands.Context = None) -> None:
        track = self.source

        if not track:
            raise NothingIsPlaying("Player is not playing anything.")

        embed = discord.Embed(title=track.title, url=track.uri, color=0x50101)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(
            name=track.author,
            url=track.uri,
            icon_url=self.client.user.display_avatar.url,
        )
        try:
            embed.set_thumbnail(url=track.thumb)
        except AttributeError:
            embed.set_thumbnail(
              url=
                "https://cdn.discordapp.com/avatars/1072443168471130132/0986983e3dc23d9d776362a929ec77dd.jpg"
            )

        embed.add_field(
            name="Length",
            value=f"{int(track.length // 60)}:{int(track.length % 60)}",
        )
        embed.add_field(name="Looping", value=self.loop)
        embed.add_field(name="Volume", value=self.volume)

        next_song = ""

        if self.loop == "CURRENT":
            next_song = self.source.title
        else:
            if len(self.queue._queue) > 0:
                next_song = self.queue._queue[0].title

        if next_song:
            embed.add_field(name="Next Song", value=next_song, inline=False)

        if not ctx:
            return await self.bound_channel.send(embed=embed)

        await ctx.send(embed=embed)


class Check:

    async def userInVoiceChannel(self, ctx, bot):
        """Check if the user is in a voice channel"""
        if ctx.author.voice:
            return True
        hacker5 = discord.Embed(
            title="Lock N Loaded",
            description=
            f"<a:astroz_cross:1072464778313879634> {ctx.author.mention} You are not connected in a voice channel",
            color=0x50101)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def botInVoiceChannel(self, ctx, bot):
        """Check if the bot is in a voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player.is_connected:
            return True
        hacker5 = discord.Embed(
            title="Lock N Loaded",
            description=
            f"<a:astroz_cross:1072464778313879634> {ctx.author.mention} I'm not connected in a voice channel",
            color=0x50101)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def botNotInVoiceChannel(self, ctx, bot):
        """Check if the bot is not in a voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not player.is_connected:
            return True
        hacker5 = discord.Embed(
            title="Lock N Loaded",
            description=
            f"<a:astroz_cross:1072464778313879634> I'm already connected in a voice channel",
            color=0x50101)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def userAndBotInSameVoiceChannel(self, ctx, bot):
        """Check if the user and the bot are in the same voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ((bot.user.id in ctx.author.voice.channel.voice_states)
                and (ctx.author.id in ctx.author.voice.channel.voice_states)):
            return True
        hacker5 = discord.Embed(
            title="Lock N Loaded",
            description=
            f"<a:astroz_cross:1072464778313879634> You are not connected in the same voice channel that the bot",
            color=0x50101)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False

    async def botIsPlaying(self, ctx, bot):
        """Check if the bot is playing"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        if player.is_playing:
            return True
        hacker5 = discord.Embed(
            title="Lock N Loaded",
            description=
            f"<a:astroz_cross:1072464778313879634> There is currently no song to replay",
            color=0x50101)
        hacker5.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        hacker5.timestamp = discord.utils.utcnow()
        await ctx.channel.send(embed=hacker5)
        return False


__all__ = (
    "WavelinkError",
    "AuthorizationFailure",
    "LavalinkException",
    "LoadTrackError",
    "BuildTrackError",
    "NodeOccupied",
    "InvalidIDProvided",
    "ZeroConnectedNodes",
    "NoMatchingNode",
    "QueueException",
    "QueueFull",
    "QueueEmpty",
)


class WavelinkError(Exception):
    """Base WaveLink Exception"""


class InvalidEqPreset(commands.CommandError):
    pass


class AuthorizationFailure(WavelinkError):
    """Exception raised when an invalid password is provided toa node."""


class LavalinkException(WavelinkError):
    """Exception raised when an error occurs talking to Lavalink."""


class LoadTrackError(LavalinkException):
    """Exception raised when an error occurred when loading a track."""


class NoLyricsFound(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class BuildTrackError(LavalinkException):
    """Exception raised when a track is failed to be decoded and re-built."""

    def __init__(self, data):
        super().__init__(data["error"])


class NodeOccupied(WavelinkError):
    """Exception raised when node identifiers conflict."""


class InvalidTimeString(commands.CommandError):
    pass


class InvalidIDProvided(WavelinkError):
    """Exception raised when an invalid ID is passed somewhere in Wavelink."""


class ZeroConnectedNodes(WavelinkError):
    """Exception raised when an operation is attempted with nodes, when there are None connected."""


class InvalidRepeatMode(commands.CommandError):
    pass


class NoMatchingNode(WavelinkError):
    """Exception raised when a Node is attempted to be retrieved with a incorrect identifier."""


class QueueIsEmpty(commands.CommandError):
    """AtLeast Have  Queue"""


class QueueException(WavelinkError):
    """Base WaveLink Queue exception."""

    pass


class QueueFull(QueueException):
    """Exception raised when attempting to add to a full Queue."""

    pass


class QueueEmpty(QueueException):
    """Exception raised when attempting to retrieve from an empty Queue."""

    pass


VoiceChannel = Union[discord.VoiceChannel, discord.StageChannel]

logger: logging.Logger = logging.getLogger(__name__)


class TrackNotFound(commands.CommandError):
    pass


class Buttons(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


#<:volume_down:1056039813712707654>

    @discord.ui.button(emoji="🔉",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def volume_button(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not connected to a voice channel.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)
        if player.is_playing:
            await player.set_volume(50)
            hacker1 = discord.Embed(
                description=
                "<a:tick:1072492486674616460> | Successfully changed player volume to : `50`",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="⏪",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def seek_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not connected to a voice channel.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            await player.seek(10 * 1000)
            hacker1 = discord.Embed(
                description=
                "<a:tick:1072492486674616460> | Seeked the current player to `10 seconds` .",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="<:jk_stop:1072904929062170634>",
                       style=discord.ButtonStyle.danger,
                       row=0)
    async def stop_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not connected to a voice channel.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            player.queue.clear()
            await player.stop()
            hacker1 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Destroyed the player.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="⏭️",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def skip_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not connected to a voice channel.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            await player.stop()
            hacker1 = discord.Embed(
                description=
                "<a:tick:1072492486674616460> | Successfully Skipped the track .",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

    @discord.ui.button(emoji="🔊",
                       style=discord.ButtonStyle.grey,
                       row=0)
    async def vol_button(self, interaction: discord.Interaction,
                         button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not connected to a voice channel.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker,
                                                           ephemeral=True)

        if player.is_playing:
            await player.set_volume(100)
            hacker1 = discord.Embed(
                description=
                "<a:tick:1072492486674616460> | Successfully changed player volume to : `100`",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker1,
                                                           ephemeral=True)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            return await interaction.response.send_message(embed=hacker2,
                                                           ephemeral=True)

        
class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.playlist = []
        self.user_timer = {}
        self.user_all_time = {}
    def help_custom(self):
		      emoji = '<:astroz_music:1085778016162029658>'
		      label = "Music"
		      description = "Shows You Music Commands"
		      return emoji, label, description
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host="eu-lavalink.lexnet.cc",
            port="443",
            password="lexn3tl@val!nk",
            https=True,
            spotify_client=spotify.SpotifyClient(
                client_id="7404513d82b4417cb851474da341cda5",
                client_secret="39820001b86f4a00822fe7c07bda642e"))
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is now ready!")
        await self.bot.loop.create_task(self.create_nodes())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")

    @commands.command(name="play", usage="play <search>", aliases=[("p")])
    @blacklist_check()
    @ignore_check()
    async def play(self, ctx: commands.Context, *, search: str):
        await ctx.defer()
        if not getattr(ctx.author, "voice", None):
            nv = discord.Embed(
                description=
                f'<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.',
                color=0x50101)
            await ctx.send(embed=nv)
            return
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player, self_deaf=True)
            embed = discord.Embed(
                description=
                f"Successfully Connected To {ctx.author.voice.channel.mention}",
                color=0x50101)
            embed.timestamp = discord.utils.utcnow()
            embed.set_thumbnail(url = f"{ctx.author.avatar}")
            await ctx.send(
                f"<a:tick:1072492486674616460> | Successfully Connected To {ctx.author.voice.channel.mention}"
            )
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.chanctx = ctx.channel

        if 'https://open.spotify.com' in str(search):

            if vc.queue.is_empty and not vc.is_playing():

                track = await spotify.SpotifyTrack.search(query=search,
                                                          return_first=True)

                await vc.play(track)

                mbed = discord.Embed(
                    color=0x50101,
                    description=
                    f"<a:Playing:1072907549428437043> [{track.title}](https://discord.gg/z7B4MXCZ9K)"
                )
                # mbed.add_field(name="<a:Playing:1072907549428437043> ", value=f"[{track.title}](https://discord.gg/z7B4MXCZ9K)")
                # mbed.add_field(name="<:jk_users:1045213273273929738> Requested By", value=f"{ctx.author.mention}")
                mbed.add_field(name="<:i_stage:1072848898357477426> Song By",
                               value=f"`{track.author}`")
                mbed.add_field(name="<:artic_uptime:1072911362428244039> Duration",
                               value=f"`❯ { round(track.duration / 60, 2)}`")
                mbed.set_author(name="NOW PLAYING",
                                icon_url=f"{ctx.author.avatar}")

                mbed.set_thumbnail(url=self.bot.user.display_avatar.url)
                mbed.set_footer(text=f"Requested By {ctx.author}",
                                icon_url=f"{ctx.author.avatar}")
                mbed.timestamp = discord.utils.utcnow()

                view = Buttons()
                await ctx.send(embed=mbed, view=view)

            else:
                track = await spotify.SpotifyTrack.search(query=search,
                                                          return_first=True)
                await vc.queue.put_wait(track)
                embed = discord.Embed(
                    description=
                    f'[{track}](https://discord.gg/z7B4MXCZ9K) Added To The Queue',
                    color=0x50101)

                embed.set_author(name="ADDED TO QUEUE",
                                 icon_url=f"{ctx.author.avatar}")
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.timestamp = discord.utils.utcnow()
                await ctx.send(embed=embed)

        elif 'https://www.youtube.com/' in str(search):

            if vc.queue.is_empty and not vc.is_playing():

                track1 = await vc.node.get_tracks(query=search,
                                                  cls=wavelink.Track)

                await vc.play(track1[0])
                mbed = discord.Embed(
                    color=0x50101,
                    description=
                    f"<a:Playing:1072907549428437043> [{track1}](https://discord.gg/z7B4MXCZ9K)"
                )
                mbed.add_field(name="Song Url", value=search)
                # mbed.add_field(name="<a:Playing:1072907549428437043> ", value=f"[{track1}](https://discord.gg/z7B4MXCZ9K)")
                mbed.set_author(name="NOW PLAYING",
                                icon_url=f"{ctx.author.avatar}")
                mbed.set_thumbnail(url=self.bot.user.display_avatar.url)
                mbed.set_footer(text=f"Requested By {ctx.author}",
                                icon_url=f"{ctx.author.avatar}")
                mbed.timestamp = discord.utils.utcnow()
                view = Buttons()
                await ctx.send(embed=mbed, view=view)

            else:
                track1 = await vc.node.get_tracks(query=search,
                                                  cls=wavelink.Track)
                await vc.queue.put_wait(track1[0])
                embed = discord.Embed(
                    description=
                    f'[{track1}](https://discord.gg/z7B4MXCZ9K) Added To The Queue',
                    color=0x50101)

                embed.set_author(name="ADDED TO QUEUE",
                                 icon_url=f"{ctx.author.avatar}")
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.timestamp = discord.utils.utcnow()
                await ctx.reply(embed=embed)

        else:

            if vc.queue.is_empty and not vc.is_playing():

                track2 = await wavelink.YouTubeTrack.search(query=search,
                                                            return_first=True)

                await vc.play(track2)

                mbed = discord.Embed(
                    color=0x50101,
                    description=
                    f"<a:Playing:1072907549428437043> [{track2.title}](https://discord.gg/z7B4MXCZ9K)"
                )
                #mbed.add_field(name="<a:Playing:1072907549428437043> ", value=f"[{track2.title}](https://discord.gg/z7B4MXCZ9K)")
                #mbed.add_field(name="<:jk_users:1045213273273929738> Requested By", value=f"{ctx.author.mention}")
                mbed.add_field(name="<:i_stage:1072848898357477426> Song By",
                               value=f"`{track2.author}`")
                mbed.add_field(name="<:artic_uptime:1072911362428244039> Duration",
                               value=f"`❯ { round(track2.duration / 60, 2)}`")
                mbed.set_thumbnail(url=track2.thumb)

                mbed.set_author(name="NOW PLAYING",
                                icon_url=f"{ctx.author.avatar}")
                mbed.set_footer(text=f"Requested By {ctx.author}",
                                icon_url=f"{ctx.author.avatar}")
                mbed.timestamp = discord.utils.utcnow()

                view = Buttons()
                await ctx.send(embed=mbed, view=view)

            else:

                track2 = await wavelink.YouTubeTrack.search(query=search,
                                                            return_first=True)
                await vc.queue.put_wait(track2)
                embed = discord.Embed(
                    description=
                    f'[{track2}](https://discord.gg/z7B4MXCZ9K) Added To The Queue',
                    color=0x50101)

                embed.set_author(name="ADDED TO QUEUE",
                                 icon_url=f"{ctx.author.avatar}")
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.timestamp = discord.utils.utcnow()
                await ctx.send(embed=embed)



    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track,
                                    reason):

        if not player.queue.is_empty:
            ctx = player.chanctx
            new_song = player.queue.get()
            await player.play(new_song)

            if hasattr(new_song, 'thumb'):
                mbed = discord.Embed(
                    color=0x50101,
                    description=
                    f"<a:Playing:1072907549428437043> [{new_song.title}](https://discord.gg/z7B4MXCZ9K)"
                )
                #mbed.add_field(name="<a:Playing:1072907549428437043> ", value=f"[{new_song.title}](https://discord.gg/z7B4MXCZ9K)")
                #mbed.add_field(name="<:jk_users:1045213273273929738> Requested By", value=f"{ctx.author.mention}")
                mbed.add_field(name="<:i_stage:1072848898357477426> Song By",
                               value=f"`{new_song.author}`")
                mbed.add_field(name="<:artic_uptime:1072911362428244039> Duration",
                               value=f"`❯ {round(new_song.duration / 60, 2)}`")

                mbed.set_author(name="NOW PLAYING",
                                icon_url=self.bot.user.display_avatar.url)
                mbed.set_thumbnail(url=new_song.thumb)
                mbed.timestamp = discord.utils.utcnow()
                view = Buttons()
                await ctx.send(embed=mbed, view=view)

            else:
                mbed = discord.Embed(
                    color=0x50101,
                    description=
                    f"<a:Playing:1072907549428437043> [{new_song.title}](https://discord.gg/z7B4MXCZ9K)"
                )
                #mbed.add_field(name="<a:Playing:1072907549428437043> ", value=f"[{new_song.title}](https://discord.gg/z7B4MXCZ9K)")
                mbed.add_field(
                    name="<:jk_users:1045213273273929738> Requested By",
                    value=f"{ctx.author.mention}")
                mbed.add_field(name="<:i_stage:1072848898357477426> Song By",
                               value=f"`{new_song.author}`")

                mbed.add_field(name="<:artic_uptime:1072911362428244039> Duration",
                               value=f"`❯ {round(new_song.duration / 60, 2)}`")

                mbed.set_author(name="NOW PLAYING",
                                icon_url=self.bot.user.display_avatar.url)
                mbed.set_thumbnail(url=new_song.thumb)
                mbed.timestamp = discord.utils.utcnow()
                view = Buttons()
                await ctx.send(embed=mbed, view=view)

    @commands.command(name="connect",
                      help="connect to your channel .",
                      aliases=["join", "j", "jvc"],
                      usage="connect [channel]")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def connect(self,
                      ctx: commands.Context,
                      *,
                      channel: discord.VoiceChannel = None):
        """Connects to a voice channel."""
        if not getattr(ctx.author, "voice", None):
            nv = discord.Embed(
                description=
                f'<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.',
                color=0x50101)
            await ctx.send(embed=nv)
            return
        if channel is None:
            channel = ctx.author.voice.channel
        elif ctx.voice_client:
            av = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am already connected to a voice channel.",
                color=0x50101)
            await ctx.send(embed=av)
            return
        vc: wavelink.Player = await channel.connect(cls=wavelink.Player,
                                                    self_deaf=True)
        sc = discord.Embed(
            description=
            f"<a:tick:1072492486674616460> | Successfully connected to {channel.mention}.",
            color=0x50101)
        await ctx.send(embed=sc)

    @commands.command(name="disconnect",
                      usage="disconnect [channel]",
                      aliases=[("dc")])
    @blacklist_check()
    @ignore_check()
    async def leave_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)

            hacker.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=hacker)

        await player.disconnect()
        hacker1 = discord.Embed(
            description=
            f"<a:tick:1072492486674616460> | Successfully disconnected from {ctx.author.voice.channel.mention}",
            color=0x50101)

        await ctx.send(embed=hacker1)

    @commands.command(name="stop", usage="stop")
    @blacklist_check()
    @ignore_check()
    async def stop_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            
            return await ctx.reply(embed=hacker)

        if player.is_playing:
            player.queue.clear()
            await player.stop()
            hacker1 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Destroyed the player.",
                color=0x50101)
        
            await ctx.send(embed=hacker1)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            
            hacker2.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=hacker2)

    @commands.command(name="skip", usage="skip", aliases=[("s")])
    @blacklist_check()
    @ignore_check()
    async def skip_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            return await ctx.reply(embed=hacker)

        if player.is_playing:
            await player.stop()
            hacker1 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully Skipped the track .",
                color=0x50101)

            await ctx.send(embed=hacker1)
        else:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                color=0x50101)
            return await ctx.reply(embed=hacker2)

    @commands.command(name="pause", usage="pause")
    @blacklist_check()
    @ignore_check()
    async def pause_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            hacker.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=hacker)

        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                hacker1 = discord.Embed(
                    description=
                    f"<a:tick:1072492486674616460> | Successfully paused the player .",
                    color=0x50101)
                view = Buttons()
                await ctx.send(embed=hacker1)
            else:
                hacker2 = discord.Embed(
                    description=
                    f"<a:astroz_cross:1072464778313879634> | I am not playing anything.",
                    color=0x50101)
                return await ctx.reply(embed=hacker2)
        else:
            hacker3 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | Player is already paused .",
                color=0x50101)

            return await ctx.reply(embed=hacker3)

    @commands.command(name="resume", usage="resume")
    @blacklist_check()
    @ignore_check()
    async def resume_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)

            
            return await ctx.reply(embed=hacker)

        if player.is_paused():
            await player.resume()
            hacker1 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Successfully resumed the player .",
                color=0x50101)

            await ctx.send(embed=hacker1)
        else:
            hacker3 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | Player is already resumed .",
                color=0x50101)
            
            return await ctx.reply(embed=hacker3)

    

    @commands.hybrid_command(name="move", usage="move <VoiceChannel>")
    @blacklist_check()
    @ignore_check()
    async def move_to(self, ctx, channel: discord.VoiceChannel) -> None:
        await ctx.guild.change_voice_state(channel=channel)
        hacker4 = discord.Embed(
            description=f"Moving to voice channel:: {channel.id} .",
            color=0x50101)

        await ctx.send(embed=hacker4)

    @commands.command(name="volume", usage="volume <vol>", aliases=[("vol")])
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def volume(self, ctx, volume):

        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        if ((not volume.isdigit()) or (int(volume)) < 0
                or (int(volume) > 500)):
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | Volume Must Be 0 To 500 .",
                color=0x50101)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            hacker.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.send(embed=hacker)
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        volume = int(volume)
        await player.set_volume(volume)
        hacker4 = discord.Embed(
            description=
            f"<a:tick:1072492486674616460> | Successfully changed player volume to : `{volume}%`",
            color=0x50101)

        await ctx.send(embed=hacker4)

    @commands.command(name="nowplaying", usage="nowplaying", aliases=[("now")])
    @blacklist_check()
    @ignore_check()
    async def playing(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | Not connected to a voice channel.",
                color=0x50101)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            hacker.set_thumbnail(url=f"{ctx.author.avatar}")
            
            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            hacker1.set_footer(text=f"Requested By {ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
            hacker1.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            hacker1 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | I am not playing anything .",
                color=0x50101)
            hacker1.set_footer(text=f"Requested By {ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker1.set_thumbnail(url=f"{ctx.author.avatar}")
            hacker1.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=hacker1)

        em = discord.Embed(
            description=f"[{vc.track}](https://discord.gg/z7B4MXCZ9K)",
            color=0x50101)

        em.add_field(name="<:i_stage:1072848898357477426> Song By",
                     value=f"`{vc.track.author}`")
        em.add_field(
            name="<:artic_uptime:1072911362428244039> Duration",
            value=f"`❯ {datetime.timedelta(seconds=vc.track.length)}`")
        em.set_footer(text=f"Requested By {ctx.author}",
                      icon_url=f"{ctx.author.avatar}")
        em.set_author(name="NOW PLAYING", icon_url=f"{ctx.author.avatar}")
        em.set_thumbnail(url=f"{ctx.author.avatar}")
        em.timestamp = discord.utils.utcnow()
        return await ctx.send(embed=em)

    @commands.command(name="shuffle", usage="shuffle", aliases=[("shuff")])
    @blacklist_check()
    @ignore_check()
    async def shuffle(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | Not connected to a voice channel.",
                color=0x50101)

            
            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)

            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        copy = vc.queue.copy()
        random.shuffle(copy)
        vc.queue = copy
        hacker2 = discord.Embed(
            description=
            "<a:tick:1072492486674616460> | Successfully shuffled the current queue .",
            color=0x50101)
        await ctx.send(embed=hacker2)

    @commands.command(name="pull", usage="pull <index>")
    @blacklist_check()
    @ignore_check()
    async def pull(self, ctx, index: int):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | Not connected to a voice channel.",
                color=0x50101)
            
            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        if index > len(vc.queue) or index < 1:
            hacker2 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | Must Be Between 1 And {len(vc.queue)} .",
                color=0x50101)
            return await ctx.reply(embed=hacker2)

        removed = vc.queue.pop(index - 1)
        hacker3 = discord.Embed(
            description=
            f"<a:tick:1072492486674616460> | Successfully pulled out `{removed.title}` From Queue .",
            color=0x50101)
        await ctx.send(embed=hacker3)

    @commands.group(name="queue", invoke_without_command=True, aliases=['q'])
    @blacklist_check()
    @ignore_check()
    async def _queue(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)

            
            return await ctx.reply(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You need to join a voice channel to play something .",
                color=0x50101)
            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            hacker3 = discord.Embed(
                description=
                f"<a:astroz_cross:1072464778313879634> | No songs in queue .",
                color=0x50101)
            hacker3.set_footer(text=f"Requested By {ctx.author}",
                               icon_url=f"{ctx.author.avatar}")
            hacker3.set_thumbnail(url = f"{ctx.author.avatar}")
            hacker3.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=hacker3)
        hacker4 = discord.Embed(title="Music | Queue", color=0x50101)
        hacker4.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        hacker4.set_thumbnail(url=f"{ctx.author.avatar}")

        copy = vc.queue.copy()
        count = 0
        for song in copy:
            count += 1
            hacker4.add_field(name=f"Position : {count}",
                              value=f"[{song.title}](https://discord.gg/z7B4MXCZ9K)")
        return await ctx.send(embed=hacker4)

    @_queue.command(name="clear", aliases=[("c")])
    @blacklist_check()
    @ignore_check()
    async def _clear(self, ctx):
        if not ctx.voice_client:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | Not connected to a voice channel.",
                color=0x50101)

            
            return await ctx.send(embed=hacker)
        elif not getattr(ctx.author.voice, "channel", None):
            hacker1 = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)

            return await ctx.send(embed=hacker1)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.queue.clear()
        hacker3 = discord.Embed(
            description=
            f"<a:tick:1072492486674616460> | Successfully Clears The current Queue .",
            color=0x50101)
        hacker3.set_footer(text=f"Requested By {ctx.author}",
                           icon_url=f"{ctx.author.avatar}")
        return await ctx.send(embed=hacker3)

    @commands.command(name="seek", aliases=["sk"], usage="seek")
    @blacklist_check()
    @ignore_check()
    async def seek_command(self, ctx, position: str):
        node = wavelink.NodePool.get_node()
        player: Player = node.get_player(ctx.guild)

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        hacker3 = discord.Embed(
            description=
            f"<a:tick:1072492486674616460> | Successfully Seeked the current player to {secs} .",
            color=0x50101)
        await ctx.reply(embed=hacker3)


    @commands.hybrid_group(name="filter",
                    invoke_without_command=True,
                    aliases=['filters'])
    @blacklist_check()
    @ignore_check()
    async def _filter(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_filter.group(name="lofi",
                    invoke_without_command=True,
                    aliases=['Lofi'])
    @blacklist_check()
    @ignore_check()
    async def _lofi(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_lofi.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def lofi_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed =  0.7500000238418579, pitch = 0.800000011920929, rate = 1)))
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled lofi filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)


    @_lofi.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmlofi_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled lofi filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            

        await ctx.reply(embed=hacker4)
      
    @_filter.group(name="bassboost",
                    invoke_without_command=True,
                    aliases=['bass'])
    @blacklist_check()
    @ignore_check()
    async def _bassboost(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_bassboost.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def bass_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            hacker.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=hacker)
        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
                 (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
                 (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)]
        await vc.set_filter(wavelink.Filter(
            equalizer=wavelink.Equalizer(name="MyOwnFilter", bands=bands)),
                            seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled bassboost filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url) 

        await ctx.reply(embed=hacker4)

    @_bassboost.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmbass_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled bassboost filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)
      
    @_filter.group(name="nightcore",
                    invoke_without_command=True,
                    aliases=['ncore'])
    @blacklist_check()
    @ignore_check()
    async def _nightcore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_nightcore.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def nightore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 1.2999999523162842, pitch = 1.2999999523163953, rate = 1)))
      
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled nightcore filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4) 

    @_nightcore.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmnightcore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled nightcore filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4) 

    @_filter.group(name="daycore",
                    invoke_without_command=True,
                    aliases=['dcore'])
    @blacklist_check()
    @ignore_check()
    async def _daycore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_daycore.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def daycore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 0.8111111111111, pitch = 0.8111111111111, rate = 1)))
      
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled daycore filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_daycore.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmdaycore_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled daycore filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_filter.group(name="speed",
                    invoke_without_command=True,
                    aliases=['Speed'])
    @blacklist_check()
    @ignore_check()
    async def _speed(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_speed.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def speed_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 1.1, pitch = 0.45555555, rate = 1.5)))
      
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled speed filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_speed.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmspeed_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled speed filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_filter.group(name="drunk",
                    invoke_without_command=True,
                    aliases=['dunk'])
    @blacklist_check()
    @ignore_check()
    async def _drunk(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_drunk.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def drunk_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 1.1, pitch = 0.45555555, rate = 1)))
      
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled drunk filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_drunk.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmdrunk_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled drunk filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_filter.group(name="quick",
                    invoke_without_command=True,
                    aliases=[''])
    @blacklist_check()
    @ignore_check()
    async def _quick(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_quick.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def quick_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 5)))
      
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled quick filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_quick.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmfloat_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled quick filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    @_filter.group(name="slowmode",
                    invoke_without_command=True,
                    aliases=['shree'])
    @blacklist_check()
    @ignore_check()
    async def _slowmode(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    
    @_slowmode.command(name="enable", aliases=[("on")])
    @blacklist_check()
    @ignore_check()
    async def pani_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            hacker = discord.Embed(
                description=
                "<a:astroz_cross:1072464778313879634> | You are not connected to a voice channel.",
                color=0x50101)
            hacker.set_footer(text=f"Requested By {ctx.author}",
                              icon_url=f"{ctx.author.avatar}")
            hacker.set_thumbnail(url = f"{ctx.author.avatar}")
            
            return await ctx.reply(embed=hacker)
          
        await vc.set_filter(wavelink.Filter(vc._filter, timescale=wavelink.Timescale(speed = 0.7, pitch = 1.0, rate = 1)))
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully enabled slowmode filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url) 

        await ctx.reply(embed=hacker4)

    @_slowmode.command(name="disable", aliases=[("off")])
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def rmpani_command(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully disabled slowmode filter .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)
    


    @_filter.command(name="reset",
                    invoke_without_command=True,
                    aliases=['lmaoded'])
    
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    async def _reset(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client

        if ctx.author.voice is None:
          hacker = discord.Embed(
                color=0x50101)
          hacker.set_author(name=f" | You are not connected to a Voice Channel .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
          return await ctx.reply(embed=hacker)
        if ctx.voice_client:
            if ctx.author.voice.channel != ctx.guild.me.voice.channel:
                hacker2 = discord.Embed(
                color=0x50101)
                hacker2.set_author(name=f" | You are not connected to the same Voice Channel as me .",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)            
                await ctx.send(embed=hacker2)
                return   

        await vc.set_filter(
            wavelink.Filter(equalizer=wavelink.Equalizer.flat()), seek=True)
        hacker4 = discord.Embed(
            color=0x50101)
        hacker4.set_author(name=f" | Successfully cleared all applied filters.",icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=hacker4)

    