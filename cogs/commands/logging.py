import discord
from discord.ext import commands
import os
import json
import random
os.system('cls')
from discord.ext.commands import Cog
import datetime
from typing import List,Union,Tuple,Dict,Any
import string
import io


def _fetch_perms(role):
  perms = []
  for perm in role.permissions:
    if perm[1]:
      xperm = string.capwords(perm[0])
      perms.append(xperm)
  permf = ", ".join(perms)
  if permf == ", ":
    return None
  return permf


def _channel_change(
        before: discord.abc.GuildChannel,
        after: discord.abc.GuildChannel,
        *,
        TYPE: str,
    ) -> List[Tuple[str, Any]]:
        ls = []
        if before.name != after.name:
            ls.append(("`Name Changed     :`", before.name))
        if before.position != after.position:
            ls.append(("`Position Changed :`", before.position))
        if before.overwrites != after.overwrites:
            ls.append(
                ("`Overwrite Changed:`", _overwrite_to_json(before.overwrites))
            )
        if (
            before.category
            and after.category
            and before.category.id != after.category.id
        ):
            ls.append(
                (
                    "`Category Changed :`"
                    if after.category
                    else "`Category Removed :`",
                    f"{before.category.name} ({before.category.id})",
                )
            )
        if before.permissions_synced is not after.permissions_synced:
            ls.append(("`Toggled Permissions Sync:`", after.permissions_synced))

        if "text" in TYPE.lower():
            if before.nsfw is not after.nsfw:
                ls.append(("`NSFW Toggled     :`", after.nsfw))
            if before.topic != after.topic:
                ls.append(("`Topic Changed    :`", after.topic))
            if before.slowmode_delay != after.slowmode_delay:
                ls.append(
                    (
                        "`Slowmode Delay Changed:`"
                        if after.slowmode_delay
                        else "`Slowmode Delay Removed:`",
                        after.slowmode_delay or None,
                    )
                )

        if "vc" in TYPE.lower():
            if before.user_limit != after.user_limit:
                ls.append(("`Limit Updated    :`", before.user_limit or None))
            if before.rtc_region != after.rtc_region:
                ls.append(
                    (
                        "`Region Updated   :`",
                        before.rtc_region if after.rtc_region is not None else "Auto",
                    )
                )
            if before.bitrate != after.bitrate:
                ls.append(("`Bitrate Updated  :`", before.bitrate))
        return ls
  
def _overwrite_to_json(
        overwrites: Dict[
            Union[discord.Role, discord.User], discord.PermissionOverwrite
        ],
    ) -> str:
        try:
            over = {
                f"{str(target.name)} ({'Role' if isinstance(target, discord.Role) else 'Member'})": overwrite._values
                for target, overwrite in overwrites.items()
            }
            return json.dumps(over, indent=4)
        except TypeError:
            return "{}"


def _update_role(before: discord.Role,
        after: discord.Role,
    ) -> List[Tuple[str, Union[int, str, bool, Tuple[int, int, int]]]]:
        ls = []
        if before.name != after.name:
            ls.append(("`Name Changed      :`", after.name))
        if before.position != after.position:
            ls.append(("`Position Changed  :`", after.position))
        if before.hoist is not after.hoist:
            ls.append(("`Hoist Toggled     :`", after.hoist))
        if before.color != after.color:
            ls.append(("`Color Changed     :`", after.color.to_rgb()))
        if before.permissions != after.permissions:
          ls.append(("`Permissions Changed     :`",_fetch_perms(after)))
        return ls

def save(method, guild, channel):
  with open("loggingbyauth.json","r") as f:
    idk = json.load(f)
  idk[str(guild)][method] = str(channel)
  with open("loggingbyauth.json","w") as f:
    json.dump(idk,f,indent=4)

def difference_list(li1: List, li2: List) -> List:
        return [i for i in li1 + li2 if i not in li1 or i not in li2]

def _member_change(before, after):
        ls = []
        if before.nick != after.nick:
            ls.append(["`Nickname Changed:`", before.nick])
        if before.name != after.name:
            ls.append(["`Name changed:`", before.name])
        if before.discriminator != after.discriminator:
            ls.append(["`Discriminator:`", before.discriminator])
        if before.display_avatar.url != after.display_avatar.url:
            ls.append(["`Avatar Changed:`", f"<{before.display_avatar.url}>"])
        if before.roles != after.roles:
            ls.append((
                "`Role Update:`",
                ", ".join(
                    [
                        role.name
                        for role in difference_list(before.roles, after.roles)
                    ]
                ),
            ))
        return ls

def _server_change(before,after):
  if after.premium_tier != before.premium_tier:
    return "False"
  ls = []
  if before.name != after.name:
    ls.append(f"Name Changed: {before.name}")
  if before.icon != after.icon:
    ls.append(f"Icon Changed: {before.icon.url if before.icon else 'None'}")
  if before.description != after.description:
    ls.append(f"Description Changed: {before.description}")
  if before.banner != after.banner:
    ls.append(f"Banner Changed: {before.banner.url if before.banner else 'None'}")
  if before.owner_id != after.owner_id:
    ls.append(f"Ownership Transferred: {before.owner.mention}")
  if after.features != before.features:
    ls.append("Features Changed")
  if "VANITY_URL" in after.features:
    if before.vanity_url_code != after.vanity_url_code:
      ls.append(f"Vanity Code Changed: {before.vanity_url_code}")
  if before.verification_level != after.verification_level:
    ls.append(f"Verification Level Changed: {before.verification_level}")
  if before.system_channel != after.system_channel:
    ls.append(f"System Channel Changed: {before.system_channel.mention if before.system_channel else 'None'}")
  if before.rules_channel != after.rules_channel:
    ls.append(f"Rules Channel Changed: {before.rules_channel.mention if before.rules_channel else 'None'}")
  if after.afk_channel != before.afk_channel:
    ls.append(f"AFK Channel Changed: {before.afk_channel.mention if before.afk_channel else 'None'}")
  if after.afk_timeout != before.afk_timeout:
    ls.append(f"AFK Timeout: {before.afk_timeout}")
  return ls

def _server_change_(bef,aft):
  before = aft
  after = bef
  if after.premium_tier != before.premium_tier:
    return "False"
  ls = []
  if before.name != after.name:
    ls.append(f"Name Changed: {before.name}")
  if before.icon != after.icon:
    ls.append(f"Icon Changed: {before.icon.url if before.icon else 'None'}")
  if before.description != after.description:
    ls.append(f"Description Changed: {before.description}")
  if before.banner != after.banner:
    ls.append(f"Banner Changed: {before.banner.url if before.banner else 'None'}")
  if before.owner_id != after.owner_id:
    ls.append(f"Ownership Transferred: {before.owner.mention}")
  if after.features != before.features:
    ls.append("Features Changed")
  if "VANITY_URL" in after.features:
    if before.vanity_url_code != after.vanity_url_code:
      ls.append(f"Vanity Code Changed: {before.vanity_url_code}")
  if before.verification_level != after.verification_level:
    ls.append(f"Verification Level Changed: {before.verification_level}")
  if before.system_channel != after.system_channel:
    ls.append(f"System Channel Changed: {before.system_channel.mention if before.system_channel else 'None'}")
  if before.rules_channel != after.rules_channel:
    ls.append(f"Rules Channel Changed: {before.rules_channel.mention if before.rules_channel else 'None'}")
  if after.afk_channel != before.afk_channel:
    ls.append(f"AFK Channel Changed: {before.afk_channel.mention if before.afk_channel else 'None'}")
  if after.afk_timeout != before.afk_timeout:
    ls.append(f"AFK Timeout: {before.afk_timeout}")
  for item in ls:
    newitem = f"{item}".replace("Changed", "")
    ls.remove(item)
    ls.append(newitem)
  return ls


def get_data(guild):
  with open("loggingbyauth.json", "r") as f:
    idk = json.load(f)
  return idk.get(str(guild))


def save_all(guild, channel):
  xc = str(channel)
  dat = {"msg": xc, "member": xc, "server": xc, "channel": xc, "role": xc, "mod": xc}
  with open("loggingbyauth.json","r") as f:
    idk = json.load(f)
  idk[str(guild)] = dat
  with open("loggingbyauth.json","w") as f:
    json.dump(idk,f,indent=4)


def save_g(guild):
  data = {"msg": None, "member": None, "server": None, "channel": None, "role": None, "mod": None}
  with open("loggingbyauth.json","r") as f:
    idk = json.load(f)
  if str(guild) in idk:
    return
  idk[str(guild)] = data
  with open("loggingbyauth.json","w") as f:
    json.dump(idk,f,indent=4)


class Logging(commands.Cog):
  def __init__(self, client):
    self.bot = client
  def help_custom(self):
		      emoji = '<:artic_logging:1072845568059113472>'
		      label = "Logging"
		      description = "Shows You Logging Commands"
		      return emoji, label, description

  async def _check(self, ctx):
    return int(ctx.message.author.top_role.position) > int(ctx.guild.me.top_role.position)

  @commands.Cog.listener()
  async def on_ready(self):
    for guild in self.bot.guilds:
      save_g(str(guild.id))

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    save_g(str(guild.id))

    
  
  @commands.command(name="logging")
  async def _loggging(self, ctx):
    message = """`msglog`
Log message deleted/ edited / bulk deleted.

`memberlog`
Log when someone joins/leaves/nickname/role update etc..

`serverlog`
Log server updates like emoji update , icon change, etc.

`channellog`
Log create/ edit/ delete channel.

`rolelog`
Log create/ edit/ delete roles.

`modlog`
Log mod actions in the server.

`logall`
Enables/Disables all the logs at once in a channel.

`logall enable`
Enables all the log in the given channel.

`logall disable`
Disables all the log in the server."""
    embed = discord.Embed(title="Logging (9)", description=message.replace("?",ctx.prefix, color=0x2f3136))
    embed.set_footer(icon_url=ctx.bot.user.avatar, text="Thanks For Choosing Ventura!")
    await ctx.send(embed=embed)


  @commands.command(name="msglog", aliases=["messagelog"])
  async def _msglog(self, ctx, channel: discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save("msg",str(ctx.guild.id),str(ctx.channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | Message log channel updated to {channel.mention}")
    
    
  @commands.command(name="memberlog", aliases=["memlog"])
  async def __msglog(self, ctx, channel: discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save("member",str(ctx.guild.id),str(ctx.channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | Member log channel updated to {channel.mention}")


  @commands.command(name="serverlog", aliases=["svlog"])
  async def ___msglog(self, ctx, channel: discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save("server",str(ctx.guild.id),str(ctx.channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | Server log channel updated to {channel.mention}")

  @commands.command(name="channellog", aliases=["chlog"])
  async def ___msglog_(self, ctx, channel: discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save("channel",str(ctx.guild.id),str(ctx.channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | Channel log channel updated to {channel.mention}")


  @commands.command(name="rolelog", aliases=["rl"])
  async def __msglog__(self, ctx, channel: discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save("role",str(ctx.guild.id),str(ctx.channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | Role log channel updated to {channel.mention}")


  @commands.command(name="modlog", aliases=["moderatelog"])
  async def teccnobetamsglog(self, ctx, channel: discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save("mod",str(ctx.guild.id),str(ctx.channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | Mod log channel updated to {channel.mention}")


  @commands.group(name="logall",invoke_without_command=True)
  async def _teknobeta(self, ctx):
    message = """`logall enable`
Enables all the log in the given channel.

`logall disable`
Disables all the log in the server."""
    embed = discord.Embed(title=f"`{ctx.prefix}`", description=message.replace("?", ctx.prefix))
    embed.set_footer(icon_url=ctx.bot.user.avatar, text="Thanks For Choosing Ventura!")
    await ctx.send(embed=embed)
    


  @_teknobeta.command(name="enable")
  async def logallenable(self,ctx,channel:discord.TextChannel):
    if not await self._check(ctx):
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    save_all(str(ctx.guild.id), str(channel.id))
    await ctx.send(f"<:ventura_tick:1084496678767300638> | All logs channel are updated to {channel.mention}")
    



  @_teknobeta.command(name="disable")
  async def _dis(self,ctx):
    if not await self._check(ctx):
      return await ctx.send("<a:astroz_cross:1072494624427483217> | Your top role should be above my top role.")
    with open("loggingbyauth.json", "r") as f:
      fl = json.load(f)
    data = fl.get(str(ctx.guild.id))
    if data == {"msg": None, "member": None, "server": None, "channel": None, "role": None, "mod": None}:
      return await ctx.reply("<a:astroz_cross:1072494624427483217> | No logging is enabled.")
    fl[str(ctx.guild.id)] = {"msg": None, "member": None, "server": None, "channel": None, "role": None, "mod": None}
    with open("loggingbyauth.json", "w") as f:
      json.dump(fl,f,indent=4)
    await ctx.reply("<:ventura_tick:1084496678767300638> | Disabled all the logs for this server.")


      


  @Cog.listener()
  async def on_raw_bulk_message_delete(self, payload, message):
    author = message.author
    msgs=list(payload.message_ids)
    embed = discord.Embed(description=f":put_litter_in_its_place: Bulk messages deleted in <#{payload.channel_id}> by {author}\n\n**Deleted Messages**\n[Click here to see deleted messages](https://discord.gg/z7B4MXCZ9K)",color=discord.Color.red())
    embed.set_author(icon_url=self.bot.user.avatar, name=f"{self.bot.user}")
    embed.set_footer(text="DELETED", icon_url=self.bot.user.avatar)
    embed.timestamp = discord.utils.utcnow()
    data = get_data(str(payload.guild_id))
    try:
      channel = self.bot.get_channel(int(data.get("msg")))
      await channel.send(embed=embed)
    except:
      pass

  def em_g(self,t,d,ft,ai,at,clr):
    embed=discord.Embed(title=t, description=d, color=clr)
    embed.set_footer(text=f"{ft}", icon_url=self.bot.user.avatar)
    embed.set_author(name=f"{ai}",icon_url=at)
    embed.timestamp = discord.utils.utcnow()
    return embed



  @Cog.listener()
  async def on_message_edit(self,before,after):
    msgobj = after
    author = after.author
    channel = after.channel
    if author.bot:
      return
    if before.content == None and after.content == None:
      return
    embed = self.em_g(None,f":pencil: Message sent by {author} edited in {channel.mention} [Jump To Message]({msgobj.jump_url})", "EDITED",author,author.avatar, clr=discord.Color.yellow())
    embed.add_field(name="Before", value=f"```{before.content}```")
    embed.add_field(name="After", value=f"```{after.content}```")
    try:
      conf = get_data(str(after.guild.id))
      channel = self.bot.get_channel(int(conf["msg"]))
      await channel.send(embed=embed)
    except Exception as w:
      print(w)
      raise w
      pass

  @Cog.listener()
  async def on_message_delete(self, message):
    author = message.author
    guild = message.guild
    if author.bot:
      return
    if message.content == None:
      return
    em = self.em_g(None, f"🚮 Message sent by {author.mention} deleted in {message.channel.mention}\n**__Content__**:\n{message.content}","DELETED", author, author.avatar, clr=discord.Color.red())
    try:
      config = get_data(str(guild.id))
      channel = self.bot.get_channel(int(config["msg"]))
      await channel.send(embed=em)
    except Exception as e:
      print(e)
      pass

  @Cog.listener()
  async def on_member_join(self, member: discord.Member):
    guild = member.guild
    embed = self.em_g("A member has joined the server", f"{member} {member.id}\n👤Account created at {discord.utils.format_dt(member.created_at)}","JOINED",member,member.avatar, clr=discord.Color.green())
    embed.set_thumbnail(url=member.avatar)
    if member.bot:
      embed.title = "**A bot has joined the server**"
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
        mem = entry.user
      embed.add_field(name="Bot added by:", value=f"{mem} - {mem.id} - {mem.mention}")
    try:
      config = get_data(str(guild.id))
      channel = self.bot.get_channel(int(config["member"]))
      await channel.send(embed=embed)
    except:
      pass

  @Cog.listener()
  async def on_member_remove(self, member):
    guild = member.guild
    kick = None
    async for logs in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
      stamp = datetime.datetime.now() - datetime.timedelta(seconds=30)
      if logs.target.id == member.id and stamp.timestamp() <= logs.created_at.timestamp():
        kick = True
        mem = logs.user
        reason = logs.reason
    TYPE_ = "LEFT" if not kick else "KICKED"
    embed = self.em_g("A member is no longer in the server", f"{member} {member.id}\n👤Account created at {discord.utils.format_dt(member.created_at)}", TYPE_, member, member.avatar, discord.Color.red())
    embed.set_thumbnail(url=member.avatar)
    if kick:
      embed2 = self.em_g("A member got kicked from the server", f"{member} {member.id}\n👤Account created at {discord.utils.format_dt(member.created_at)}", TYPE_, member, member.avatar, discord.Color.red())
      embed2.set_thumbnail(url=member.avatar)
      embed2.title = "A member got kicked from the server"
      embed2.add_field(name="Kicked by:",value=f"{mem}")
      if reason:
        embed2.add_field(name="Reason", value=f"{reason}")
        try:
          config = get_data(str(guild.id))
          channel = self.bot.get_channel(int(config["member"]))
          if kick:
            await channel.send(embed=embed)
            await channel.send(embed=embed2)
          else:
            await channel.send(embed=embed)
        except:
          pass
        

  @Cog.listener()
  async def on_guild_update(self, before,after):
    changes = "".join(f"{i} {j}\n" for i, j in _server_change(before, after))
    changes = _server_change(before, after)
    bec = "".join(f"{i} {j}\n" for i, j in _server_change_(before, after))
    bec = _server_change_(before, after)
    if changes == "False" or changes == []:
      return
    async for logs in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
      mem = logs.user
      reason = logs.reason
    em = self.em_g("Server Updated", f"Updated by: {mem}\nReason: {reason}","UPDATED",mem,mem.avatar, discord.Color.green())
    em.add_field(name="Before:", value=f"{changes}")
    em.add_field(name="After:", value=f"{bec}")
    try:
      config = get_data(str(after.id))
      channel = self.bot.get_channel(int(config["server"]))
      await channel.send(embed=em)
    except:
      pass

  @Cog.listener()
  async def on_guild_role_create(self, role):
    guild = role.guild
    async for logs in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
      if logs.target.id == role.id:
        embed = self.em_g(None, f" Role {role.mention} created by {logs.user.mention}", "ROLE CREATE", logs.user, logs.user.avatar, discord.Color.green())
        embed.add_field(name="Name", value=f"{role.name} (ID: {role.id})")
        embed.add_field(name="Color", value=f"{role.color}")
        embed.add_field(name="Mentionable", value=f"{role.mentionable}")
        embed.add_field(name="Displayed seperately", value=f"{role.hoist}")
        embed.add_field(name="Position", value=f"{role.position}")
        try:
          data = get_data(str(guild.id))
          channel = self.bot.get_channel(int(data['role']))
          await channel.send(embed=embed)
        except:
          pass

  @Cog.listener()
  async def on_guild_role_delete(self, role):
    guild = role.guild
    async for logs in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
      if logs.target.id == role.id:
        embed = self.em_g(None, f"Role {role.mention} deleted by {logs.user.mention}", "ROLE DELETE", logs.user, logs.user.avatar, discord.Color.red())
        embed.add_field(name="Name", value=f"{role.name} (ID: {role.id})")
        embed.add_field(name="Color", value=f"{role.color}")
        embed.add_field(name="Mentionable", value=f"{role.mentionable}")
        embed.add_field(name="Displayed seperately", value=f"{role.hoist}")
        embed.add_field(name="Position", value=f"{role.position}")
        embed.add_field(name="Members", value=f"{len(role.members)}")
        try:
          data = get_data(str(guild.id))
          channel = self.bot.get_channel(int(data['role']))
          await channel.send(embed=embed)
        except:
          pass


  @Cog.listener()
  async def on_guild_role_update(self, before, after):
    async for logs in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
      if after.id == logs.target.id:
        user = logs.user
        ls = _update_role(before, after)
        sex = "".join(f"{i} **{j}**\n" for i, j in ls)
        reason = logs.reason
        entryID = logs.id
        tecnomerabetahai = f""""""
        embed = self.em_g(None, tecnomerabetahai, "ROLE UPDATED", user, user.avatar, discord.Color.yellow())
        embed.add_field(name="Changes Made:", value=sex)
        try:
          con = get_data(str(after.id))
          channel = self.bot.get_channel(int(con['role']))
          await channel.send(embed=embed)
        except:
          pass

  @Cog.listener()
  async def on_guild_channel_create(self, channel):
    async for logs in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
      if logs.target.id == channel.id:
        user = logs.user
        reason = logs.reason
        entryID = logs.id
        channel_type = str(channel.type)
        TYPE = channel_type.replace("_", " ").title() + " Channel"
        data = f""""""
        embed = self.em_g(None, f"New text channel ({channel.mention}) created by {user.mention}", "CHANNEL CREATE", user, user.avatar, discord.Color.green())
        embed.add_field(name="Name", value=f"{channel.name} (ID: {channel.id})")
        embed.add_field(name="Position", value=f"{channel.position}")
        embed.add_field(name="Category", value=f"{channel.category} (ID: {channel.category.id})")
        fp = io.BytesIO(_overwrite_to_json(channel.overwrites).encode())
        fpp = fp or None
        try:
          data = get_data(str(channel.guild.id))
          channel = self.bot.get_channel(int(data['channel']))
          if fpp != "{}":
            None
            await channel.send(embed=embed)
          else:
              return "DED"
        except:
          pass
        
  @Cog.listener()
  async def on_guild_channel_delete(self, channel):
    async for logs in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
      if logs.target.id == channel.id:
        user = logs.user
        reason = logs.reason
        entryID = logs.id
        deleted_at = logs.created_at
        channel_type = str(channel.type)
        TYPE = channel_type.replace("_", " ").title() + " Channel"
        data = f""""""
        embed = self.em_g(None, f"A text channel has been deleted by {user.mention}", "CHANNEL DELETE", user, user.avatar, discord.Color.red())
        embed.add_field(name="Name", value=f"{channel.name} (ID: {channel.id})")
        embed.add_field(name="Position", value=f"{channel.position}")
        embed.add_field(name="Category", value=f"{channel.category} (ID: {channel.category.id})")
        fp = io.BytesIO(_overwrite_to_json(channel.overwrites).encode())
        fp = fp or "{}"
        try:
          data = get_data(str(channel.guild.id))
          channel = self.bot.get_channel(int(data['channel']))
          await channel.send(embed=embed)
        except:
          pass

  @Cog.listener()
  async def on_guild_channel_update(self,before,after):
    async for logs in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
      if after.id == logs.target.id:
        user = logs.user
        entryID = logs.id
        channel_type = str(after.type)
        reason = logs.reason
        TYPE = channel_type.replace("_", " ").title() + " Channel"
        ls = _channel_change(before, after, TYPE=channel_type)
        channel = after
        ext = "".join(f"{i} **{j}**\n" for i, j in ls)
        data = f""""""
        embed = self.em_g(None, data, "UPDATE", user, user.avatar, discord.Color.yellow())
        embed.add_field(name="Changes Made", value=ext)
        try:
          cnf = get_data(str(after.guild.id))
          channel = self.bot.get_channel(int(cnf["channel"]))
        except:
          pass



