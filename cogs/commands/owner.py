from __future__ import annotations
from discord.ext import commands
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import json, discord
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator

from typing import Optional


class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client
      
    @commands.command(name="slist")
    @commands.is_owner()
    async def slist(self, ctx):
        devansh37 = ([devansh for devansh in self.client.guilds])
        devansh37 = sorted(devansh37,
                         key=lambda devansh: devansh.member_count,
                         reverse=True)
        entries = [
            f"`[{i}]` | [{g.name}](https://discord.com/channels/{g.id}) - {g.member_count}"
            for i, g in enumerate(devansh37, start=1)
        ]
        paginator = Paginator(source=DescriptionEmbedPaginator(
            entries=entries,
            description="",
            title=f"Server List of Ventura - {len(self.client.guilds)}",
            color=0x2f3136,
            per_page=10),
                              ctx=ctx)
        await paginator.paginate()

    



    @commands.command(name="restart", help="Restarts the client.")
    @commands.is_owner()
    async def _restart(self, ctx: Context):
        await ctx.reply("Restarting!")
        restart_program()

    @commands.command(name="sync", help="Syncs all database.")
    @commands.is_owner()
    async def _sync(self, ctx):
        await ctx.reply("Syncing...", mention_author=False)
        with open('anti.json', 'r') as f:
            data = json.load(f)
        for guild in self.client.guilds:
            if str(guild.id) not in data['guild']:
                data['guilds'][str(guild.id)] = 'on'
                with open('anti.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                pass
        with open('config.json', 'r') as f:
            data = json.load(f)
        for op in data["guilds"]:
            g = self.client.get_guild(int(op))
            if not g:
                data["guilds"].pop(str(op))
                with open('config.json', 'w') as f:
                    json.dump(data, f, indent=4)

    @commands.group(name="blacklist",
                    help="let's you add someone in blacklist",
                    aliases=["bl"])
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
                entries = [
                    f"`[{no}]` | <@!{mem}> (ID: {mem})"
                    for no, mem in enumerate(blacklist['ids'], start=1)
                ]
                paginator = Paginator(source=DescriptionEmbedPaginator(
                    entries=entries,
                    title=
                    f"List of Blacklisted users of lock N Loaded - {len(blacklist['ids'])}",
                    description="",
                    per_page=10,
                    color=0x50101),
                                      ctx=ctx)
                await paginator.paginate()

    @blacklist.command(name="add")
    @commands.is_owner()
    async def blacklist_add(self, ctx: Context, member: discord.Member):
        try:
            with open('blacklist.json', 'r') as bl:
                blacklist = json.load(bl)
                if str(member.id) in blacklist["ids"]:
                    embed = discord.Embed(
                        title="Error!",
                        description=f"{member.name} is already blacklisted",
                        color=discord.Colour(0x50101))
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    add_user_to_blacklist(member.id)
                    embed = discord.Embed(
                        title="Blacklisted",
                        description=f"Successfully Blacklisted {member.name}",
                        color=discord.Colour(0x50101))
                    with open("blacklist.json") as file:
                        blacklist = json.load(file)
                        embed.set_footer(
                            text=
                            f"There are now {len(blacklist['ids'])} users in the blacklist"
                        )
                        await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Error!",
                                  description=f"An Error Occurred",
                                  color=discord.Colour(0x50101))
            await ctx.reply(embed=embed, mention_author=False)

    @blacklist.command(name="remove")
    @commands.is_owner()
    async def blacklist_remove(self, ctx, member: discord.Member = None):
        try:
            remove_user_from_blacklist(member.id)
            embed = discord.Embed(
                title="User removed from blacklist",
                description=
                f"<a:tick:1072492486674616460> | **{member.name}** has been successfully removed from the blacklist",
                color=0x50101)
            with open("blacklist.json") as file:
                blacklist = json.load(file)
                embed.set_footer(
                    text=
                    f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"**{member.name}** is not in the blacklist.",
                color=0x50101)
            embed.set_thumbnail(url=f"{self.client.user.display_avatar.url}")
            await ctx.reply(embed=embed, mention_author=False)

    @commands.group(
        name="np",
        help="Allows you to add someone in no prefix list (owner only command)"
    )
    @commands.is_owner()
    async def _np(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_np.command(name="list")
    @commands.is_owner()
    async def np_list(self, ctx):
        with open("info.json") as f:
            np = json.load(f)
            nplist = np["np"]
            npl = ([await self.client.fetch_user(nplu) for nplu in nplist])
            npl = sorted(npl, key=lambda nop: nop.created_at)
            entries = [
                f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) (ID: {mem.id})"
                for no, mem in enumerate(npl, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"No Prefix of lock N Loaded - {len(nplist)}",
                description="",
                per_page=10,
                color=0x50101),
                                  ctx=ctx)
            await paginator.paginate()

    @_np.command(name="add", help="Add user to no prefix")
    @commands.is_owner()
    async def np_add(self, ctx, user: discord.User):
        with open('info.json', 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id in np:
            embed = discord.Embed(
                description=
                f"**The User You Provided Already In My No Prefix**",
                color=0x50101)
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].append(user.id)
        with open('info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed1 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Added no prefix to {user} for all",
                color=0x50101)
          
            await ctx.reply(embed=embed1)

    @_np.command(name="remove", help="Remove user from no prefix")
    @commands.is_owner()
    async def np_remove(self, ctx, user: discord.User):
        with open('info.json', 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id not in np:
            embed = discord.Embed(
                description="**{} is not in no prefix!**".format(user),
                color=0x50101)
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].remove(user.id)
        with open('info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed2 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Removed no prefix from {user} for all",
                color=0x50101)

            await ctx.reply(embed=embed2)

    @commands.group(name="bdg", help="Allows owner to add badges for a user")
    @commands.is_owner()
    async def _badge(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_badge.command(name="add",
                    aliases=["give"],
                    help="Add some badges to a user.")
  
  
    @commands.is_owner()
    async def badge_add(self, ctx, member: discord.Member, *, badge: str):
        ok = getbadges(member.id)
        if badge.lower() in ["dev", "developer", "devp"]:
            idk = "**<a:dev:1072465734338363463>・DEVELOPER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed2 = discord.Embed(
        
          
    
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `Developer` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed2)
        elif badge.lower() in ["king", "owner"]:
            idk = "**<:PartnerProgramBlack:1099310514892447835> ・OWNER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `OWNER` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed8)
        elif badge.lower() in ["co", "coowner"]:
            idk = "**<:6023xmaspartnerbadge:1099310774217879572>・CO OWNER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed12 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `CO OWNER` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed12)
        elif badge.lower() in ["admin", "ad"]:
            idk = "**<:fst_admin:1099311001163276429>・ADMIN**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed20 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `ADMIN` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed20)
        elif badge.lower() in ["mods", "moderator"]:
            idk = "**<a:Moderation:1099311401610268713>・MODERATOR**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed15 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `MODERATOR` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed15)
                          
          
       
            
        
        elif badge.lower() in ["staff", "support staff"]:
            idk = "**<a:ventura_staff:1072720458585223279>・STAFF**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed3 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `STAFF` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed3)
        elif badge.lower() in ["partner"]:
            idk = "**<:PartneredServerOwner:1072720583973949511>・PARTNER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed4 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `PARTNER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed4)
        elif badge.lower() in ["sponsor"]:
            idk = "**<a:diamond:1073099102193197086>・SPONSER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed5 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `SPONSER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed5)
        elif badge.lower() in [
                "friend", "friends", "homies", "owner's friend"
        ]:
            idk = "**<:ventura_friends:1073099248410841150>・FRIENDS**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed1 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `FRIENDS` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed1)
        elif badge.lower() in ["early", "supporter", "support"]:
            idk = "**<a:astroz_early:1073099540221141084>・SUPPORTER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed6 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `SUPPORTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed6)

        elif badge.lower() in ["vip"]:
            idk = "**<:icons_vip:1099311680191725658>・VIP**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed7 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `VIP` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed7)

        elif badge.lower() in ["bug", "hunter"]:
            idk = "**<a:astroz_bug:1073100013938409482>・BUG HUNTER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `BUG HUNTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed8)
        elif badge.lower() in ["all"]:
            idk = "**<a:dev:1072465734338363463>・DEVELOPER\n<:PartnerProgramBlack:1099310514892447835>・OWNER\n<:6023xmaspartnerbadge:1099310774217879572>・CO OWNER\n<:fst_admin:1099311001163276429>・ADMIN\n<a:Moderation:1099311401610268713>・MODERATOR\n<a:ventura_staff:1072720458585223279>・STAFF\n<:PartneredServerOwner:1072720583973949511>・PARTNER\n<a:diamond:1073099102193197086>・SPONSER\n<:ventura_friends:1073099248410841150>・FRIENDS\n<a:astroz_early:1073099540221141084>・SUPPORTER\n<:icons_vip:1099311680191725658>・VIP\n<a:astroz_bug:1073100013938409482>・BUG HUNTER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embedall = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Added `All` Badges To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embedall)
        else:
            hacker = discord.Embed(
                                   description="**Invalid Badge**",
                                   color=0x50101)
            
            await ctx.reply(embed=hacker)

    @_badge.command(name="remove",
                    help="Remove badges from a user.",
                    aliases=["re"])
    @commands.is_owner()
    async def badge_remove(self, ctx, member: discord.Member, *, badge: str):
        ok = getbadges(member.id)
        if badge.lower() in ["own", "owner", "king"]:
            idk = "**<:crown1:1072718187147300924> OWNER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed2 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `OWNER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed2)

        elif badge.lower() in ["staff", "support staff"]:
            idk = "**<a:ventura_staff:1072720458585223279> STAFF**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed3 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `STAFF` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed3)

        elif badge.lower() in ["partner"]:
            idk = "**<:PartneredServerOwner:1072720583973949511> PARTNER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed4 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `PARTNER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed4)

        elif badge.lower() in ["sponsor"]:
            idk = "**<a:diamond:1073099102193197086> SPONSER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed5 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `SPONSER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed5)

        elif badge.lower() in [
                "friend", "friends", "homies", "owner's friend"
        ]:
            idk = "**<:ventura_friends:1073099248410841150> FRIENDS**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed1 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `FRIENDS` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed1)

        elif badge.lower() in ["early", "supporter", "support"]:
            idk = "**<a:astroz_early:1073099540221141084> SUPPORTER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed6 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `SUPPORTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed6)

        elif badge.lower() in ["vip"]:
            idk = "**<:VIP:1073099724678242355> VIP**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed7 = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `VIP` Badge To {member}**",
                color=0x50101)
           
            await ctx.reply(embed=embed7)

        elif badge.lower() in ["bug", "hunter"]:
            idk = "**<a:astroz_bug:1073100013938409482> BUG HUNTER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"**Successfully Removed `BUG HUNTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed8)
        elif badge.lower() in ["all"]:
            idk = "**<:crown1:1072718187147300924> OWNER\n<a:ventura_staff:1072720458585223279> STAFF\n<:PartneredServerOwner:1072720583973949511> PARTNER\n<a:diamond:1073099102193197086> SPONSER\n<:ventura_friends:1073099248410841150> FRIENDS\n<a:astroz_early:1073099540221141084> SUPPORTER\n<:VIP:1073099724678242355> VIP\n<a:astroz_bug:1073100013938409482> BUG HUNTER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embedall = discord.Embed(
                
                description=
                f"<a:tick:1072492486674616460> | **Successfully Removed `All` Badges From {member}**",
                color=0x50101)
            await ctx.reply(embed=embedall)
        else:
            hacker = discord.Embed(
                                   description="**Invalid Badge**",
                                   color=0x50101)
            await ctx.reply(embed=hacker)




    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User, *, message: str):
        """ DM the user of your choice """
        try:
            await user.send(message)
            await ctx.send(f"<a:tick:1072492486674616460> | Successfully Sent a DM to **{user}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")           



    @commands.group()
    @commands.is_owner()
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
            
            
    @change.command(name="nickname")
    @commands.is_owner()
    async def change_nickname(self, ctx, *, name: str = None):
        """ Change nickname. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"<a:tick:1072492486674616460> | Successfully changed nickname to **{name}**")
            else:
                await ctx.send("<a:tick:1072492486674616460> | Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)



    @commands.command()
    @commands.is_owner()
    async def globalban(self, ctx, *, user: discord.User = None):
        if user is None:
            return await ctx.send(
                "You need to define the user"
            )
        for guild in self.client.guilds:
            for member in guild.members:
                if member == user:
                    await user.ban(reason="lund le lo")
                  
    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def changestatus(self, ctx: commands.Context, *, status: str):
        await self.client.change_presence(
            activity=discord.Game(name=status),
            status=discord.Status.online
        )
        await ctx.message.add_reaction('<:ventura_tick:1084496678406590464>') 


    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def listening(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
            
            
        
        await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully Changed the bot's presence to Listening", color=0x030404))


    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def streaming(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=status, url = "https://www.twitch.tv/#"))
            
            
        
        await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully Changed the bot's presence to Streaming.", color=0x030404))

    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def watching(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            
            
        
        await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully Changed the bot's presence to Watching.", color=0x030404))


    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def playing(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
            
            
        
        await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully Changed the bot's presence to Playing.", color=0x030404))


    @commands.is_owner()
    @commands.command(help="Change the bot's status")
    async def competing(self, ctx: commands.Context, *, status: str):
        await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status))
            
            
        
        await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully Changed the bot's presence to Competing.", color=0x030404))



    @commands.group(
        name="apre",
        help="Allows you to add user in premium list)"
    )
    @commands.is_owner()
    async def _apre(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_apre.command(name="list")
    @commands.is_owner()
    async def apre_list(self, ctx):
        with open("info.json") as f:
            apre = json.load(f)
            aprelist = apre["apre"]
            aprel = ([await self.client.fetch_user(nplu) for aprelu in aprelist])
            aprel = sorted(aprel, key=lambda nop: nop.created_at)
            entries = [
                f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) (ID: {mem.id})"
                for no, mem in enumerate(npl, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Premium list of Lock N Loaded - {len(aprelist)}",
                description="",
                per_page=10,
                color=0x50101),
                                  ctx=ctx)
            await paginator.paginate()

    @_apre.command(name="add", help="Add user to my premium list")
    @commands.is_owner()
    async def apre_add(self, ctx, user: discord.User):
        with open('info.json', 'r') as idk:
            data = json.load(idk)
        apre = data["apre"]
        if user.id in apre:
            embed = discord.Embed(
                description=
                f"**The mentioned user is already in my premium list**",
                color=0x50101)
            await ctx.reply(embed=embed)
            return
        else:
            data["apre"].append(user.id)
        with open('info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed3110 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Added {user} to the premium list",
                color=0x50101)
          
            await ctx.reply(embed=embed3110)

    @_apre.command(name="remove", help="Remove user from premium list")
    @commands.is_owner()
    async def apre_remove(self, ctx, user: discord.User):
        with open('info.json', 'r') as idk:
            data = json.load(idk)
        apre = data["apre"]
        if user.id not in apre:
            embed = discord.Embed(
                description="**{} is not in premium list**".format(user),
                color=0x50101)
            await ctx.reply(embed=embed)
            return
        else:
            data["apre"].remove(user.id)
        with open('info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed1310 = discord.Embed(
                description=
                f"<a:tick:1072492486674616460> | Removed {user} from premium list",
                color=0x50101)

            await ctx.reply(embed=embed1310)

    @commands.is_owner()
    @commands.command()
    async def leaveguild(self, ctx, guild:discord.Guild=None):
     if ctx.author.id == 1069332033928708206:
      #try:
      if guild is None:
        await ctx.send(embed=discord.Embed(description="<a:astroz_cross:1072464778313879634> | Please provide me a server id", color=0x030404))
      else:
         await ctx.send(embed=discord.Embed(description="<:ventura_tick:1084496678406590464> | Successfully Left The Guild.", color=0x030404))
         await guild.leave()

     else:
       await ctx.send(embed=discord.Embed( color=0x030404, description="This command can be only executed by my developer"))
    
       
    





      
        
      
    
         
            
        
                       
               
        
