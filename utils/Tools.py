import json, sys, os
import discord
from discord.ext import commands
from core import Context
import aiohttp
from discord.ui import Select, View, Button
import time

from typing import Any


class NotVoter(commands.CheckFailure):
    pass


async def check_voter(mem):
    async with aiohttp.ClientSession(
            headers=
        {
            "Authorization":
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwMTI2MjcwODgyMzIxNjUzNzYiLCJib3QiOnRydWUsImlhdCI6MTY3MDU4MzE3NH0.WULUKASz45RZduUMpTCqzHt0nPk3MqnpeJHF3YNgBo8"
        }) as session:
        async with session.get(
                f"https://top.gg/api/bots/1012627088232165376/check?userId={str(mem)}"
        ) as response:
            vote = await response.json()
            if vote["voted"] == 1 or mem in []:
                response.close()
                return "okay"
            else:
                response.close()
                return "not okay"


def is_voter():

    async def predicate(ctx: Context):
        async with aiohttp.ClientSession(
                headers=
            {
                "Authorization":
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwMTI2MjcwODgyMzIxNjUzNzYiLCJib3QiOnRydWUsImlhdCI6MTY3MDU4MzE3NH0.WULUKASz45RZduUMpTCqzHt0nPk3MqnpeJHF3YNgBo8"
            }) as session:
            async with session.get(
                    f"https://top.gg/api/bots/1012627088232165376/check?userId={str(ctx.author.id)}"
            ) as response:
                vote = await response.json()
                if vote["voted"] == 1 or ctx.author.id in ctx.bot.owner_ids:
                    response.close()
                    return True
                else:
                    response.close()
                    raise NotVoter()

    return commands.check(predicate)


def DotEnv(query: str):
    return os.getenv(query)


def updateDB(guildID, data):
    with open("database.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("database.json", "w") as config:
        config.write(newdata)


def getDB(guildID):
    with open("database.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "welcome": {
                "autodel": 0,
                "channel": [],
                "color": "",
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> Welcome To <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
            },
            "autorole": {
                "bots": [],
                "humans": []
            },
            "vcrole": {
                "bots": "",
                "humans": ""
            },
            "logging": {
                "logall": False,
                "channel": [],
                "msglog": [],
                "memberlog": [],
                "serverlog": [],
                "rolelog": [],
                "channellog": [],
                "modlog": [],
                "voicelog": []
            }
        }
        updateDB(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "antiSpam": False,
            "antiLink": False,
            "whitelisted": [],
            "punishment": "ban",
            "prefix": "@",
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "owner": None,
            "coown": None,
            "headadmin": None,
            "admin": None,
            "mod": None,
            "gmod": None,
            "gadmin": None,
            "headmod": None,
            "wlrole": None
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)


def add_user_to_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        if str(user_id) in file_data["ids"]:
            return

        file_data["ids"].append(str(user_id))
    with open("blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(str(user_id))
    with open("blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)


def update_vanity(guild, code):
    with open('vanity.json', 'r') as vanity:
        vanity = json.load(vanity)
    vanity[str(guild)] = str(code)
    new = json.dumps(vanity, indent=4, ensure_ascii=False)
    with open('vanity.json', 'w') as vanity:
        vanity.write(new)


def blacklist_check():

    def predicate(ctx):
        with open("blacklist.json") as f:
            data = json.load(f)
            if str(ctx.author.id) in data["ids"]:
                return False
            return True

    return commands.check(predicate)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def getbadges(userid):
    with open("badges.json", "r") as f:
        data = json.load(f)
    if str(userid) not in data:
        default = []
        makebadges(userid, default)
        return default
    return data[str(userid)]


def makebadges(userid, data):
    with open("badges.json", "r") as f:
        badges = json.load(f)
    badges[str(userid)] = data
    new = json.dumps(badges, indent=4, ensure_ascii=False)
    with open("badges.json", "w") as w:
        w.write(new)


def getanti(guildid):
    with open("anti.json", "r") as config:
        data = json.load(config)
    if str(guildid) not in data["guilds"]:
        default = "off"
        updateanti(guildid, default)
        return default
    return data["guilds"][str(guildid)]


def updateanti(guildid, data):
    with open("anti.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildid)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("anti.json", "w") as config:
        config.write(newdata)


class Timer:
    __slots__ = ("start_time", "end_time")

    def __init__(self) -> None:
        self.start_time: float | None = None
        self.end_time: float | None = None

    def __enter__(self):
        self.start()
        return self

    async def __aenter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.stop()

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.stop()

    def start(self) -> None:
        self.start_time = time.perf_counter()

    def stop(self) -> None:
        self.end_time = time.perf_counter()

    def __str__(self) -> str:
        return str(self.total_time)

    def __int__(self) -> int:
        return int(self.total_time)

    def __repr__(self) -> str:
        return f"<Timer time={self.total_time}>"

    @property
    def total_time(self) -> float:
        if self.start_time is None:
            raise ValueError("Timer has not been started")
        if self.end_time is None:
            raise ValueError("Timer has not been stopped")
        return self.end_time - self.start_time


def format_seconds(seconds: float, *, friendly: bool = False) -> str:

    seconds = round(seconds)

    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)

    days, hours, minutes, seconds = (
        round(day),
        round(hour),
        round(minute),
        round(second),
    )

    if friendly:
        day = f"{days}d " if days != 0 else ""
        hour = f"{hours}h " if hours != 0 or days != 0 else ""
        minsec = f"{minutes}m {seconds}s"
        return f"{day}{hour}{minsec}"
    day = f"{days:02d}:" if days != 0 else ""
    hour = f"{hours:02d}:" if hours != 0 or days != 0 else ""
    minsec = f"{minutes:02d}:{seconds:02d}"
    return f"{day}{hour}{minsec}"


def updatelog(guildID, data):
    with open("logging.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("logging.json", "w") as config:
        config.write(newdata)





def add_channel_to_ignore(user_id: int) -> None:
    with open("ignore.json", "r") as file:
        file_data = json.load(file)
        if str(user_id) in file_data["ids"]:
            return

        file_data["ids"].append(str(user_id))
    with open("ignore.json", "w") as file:
        json.dump(file_data, file, indent=4)


def remove_channel_from_ignore(user_id: int) -> None:
    with open("ignore.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(str(user_id))
    with open("ignore.json", "w") as file:
        json.dump(file_data, file, indent=4)


def ignore_check():

    def predicate(ctx):
        with open("ignore.json") as f:
            data = json.load(f)
            if str(ctx.channel.id) in data["ids"]:
                return False
            return True

    return commands.check(predicate)

def getlogger(guildid):
  with open("logs.json", "r") as ok:
    data = json.load(ok)
  if str(guildid) not in data:
    default = {
      "channel": ""
    }
    makelogger(guildid, default)
    return default
  return data[str(guildid)]

def makelogger(guildid, data):
  with open("logs.json", "r") as f:
    logs = json.load(f)
  logs[str(guildid)] = data
  new = json.dumps(logs, indent=4, ensure_ascii=False)
  with open("logs.json", "w") as idk:
    idk.write(new)