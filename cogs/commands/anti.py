from __future__ import annotations
from discord.ext import commands
from core import Cog, Ventura, Context
import discord
from utils.Tools import *
from discord.ui import Button, View
import datetime
from typing import Optional
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator


class Security(Cog):
    """Shows a list of commands regarding antinuke"""

    def __init__(self, client: Ventura):
        self.client = client

    @commands.group(name="Antinuke",
                    aliases=["anti", "Security"],
                    help="Enables/Disables antinuke in your server!",
                    invoke_without_command=True,
                    usage="Antinuke Enable/Disable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _antinuke(self, ctx: Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_antinuke.command(
        name="enable",
        help="Server owner should enable antinuke for the server!",
        usage="Antinuke Enable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_enable(self, ctx: Context):
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        wled = d2["whitelisted"]
        punish = d2["punishment"]
        wlrole = d2['wlrole']
        hacker = ctx.guild.get_member(ctx.author.id)
        wlroles = ctx.guild.get_role(wlrole)

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data == "on":
                embed = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"**{ctx.guild.name} Security Settings **<:role:1072490444879056998>\nOhh uh! looks like your server has already enabled security\n\nCurrent Status: <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n\n> To disable use `antinuke disable`",
                    color=0x50101)

                await ctx.reply(embed=embed, mention_author=False)
            else:
                data = "on"
                updateanti(ctx.guild.id, data)
                embed2 = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"**{ctx.guild.name} Security Settings** <:role:1072490444879056998>\nAlso move my role to top of roles for me to work properly.\n\nPunishments:\n\n**Anti Bot:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Ban:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Kick:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Prune:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Channel Create/Delete/Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Role Create/Delete/Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Webhook Create:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Emoji Create/Delete/Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Guild Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Community Spam:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Integration Create:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Everyone/Here/Role Mention:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Whitelisted Users:** {len(wled)}\n\n**Auto Recovery:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>",
                    color=0x50101)
                embed2.add_field(
                    name="Other Settings",
                    value=
                    f"To change the punishment type `{ctx.prefix}Antinuke punishment set <type>`\nAvailable Punishments are `Ban`, `Kick` and `None`."
                )
                embed2.set_footer(text=f"Current punishment type is {punish}")
                await ctx.reply(embed=embed2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5, mention_author=False)

    @_antinuke.command(
        name="disable",
        help="You can disable antinuke for your server using this command",
        aliases=["off"],
        usage="Antinuke disable")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_disable(self, ctx: Context):
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if data == "off":
                emb = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"**{ctx.guild.name} Security Settings **<:role:1072490444879056998>\nOhh NO! looks like your server has already disabled security\n\nCurrent Status: <:6045discorddisabled:1072491417722691665>\n\n> To enable use `antinuke enable`",
                    color=0x50101)
                await ctx.reply(embed=emb, mention_author=False)
            else:
                data = "off"
                updateanti(ctx.guild.id, data)
                final = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"**{ctx.guild.name} Security Settings** <:role:1072490444879056998>\nSuccessfully disabled security settings.\n\nCurrent Status: <:6045discorddisabled:1072491417722691665>\n\n> To enable again use `antinuke enable`",
                    color=0x50101)
                await ctx.reply(embed=final, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5, mention_author=False)

    @_antinuke.command(
        name="show",
        help="Shows currently antinuke config settings of your server",
        aliases=["config"],
        usage="Antinuke show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def antinuke_show(self, ctx: Context):
        data = getanti(ctx.guild.id)
        d2 = getConfig(ctx.guild.id)
        wled = d2["whitelisted"]
        punish = d2["punishment"]
        wlrole = d2['wlrole']
        wlroles = ctx.guild.get_role(wlrole)
        if data == "off":
            emb = discord.Embed(
                title="Lock N Loaded",
                description=
                f"**{ctx.guild.name} Security Settings **<:role:1072490444879056998>\nOhh NO! looks like your server has already disabled security\n\nCurrent Status: <:6045discorddisabled:1072491417722691665>\n\n> To enable use `antinuke enable`",
                color=0x50101)
            await ctx.reply(embed=emb, mention_author=False)
        elif data == "on":
            embed2 = discord.Embed(
                title="Lock N Loaded",
                description=
                f"**{ctx.guild.name} Security Settings** <:role:1072490444879056998>\nPunishments:\n**Anti Bot:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Ban:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Kick:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Prune:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Channel Create/Delete/Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Role Create/Delete/Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Webhook Create:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Emoji Create/Delete/Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Guild Update:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Community Spam:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Integration Create:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Everyone/Here/Role Mention:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Anti Vanity Steal:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>\n**Whitelisted Role:** <@&{wlrole}>\n**Whitelisted Users:** {len(wled)}\n\n**Auto Recovery:** <:ventura_no:1072490608939257866><:ventura_yes:1072490699452334100>",
                color=0x50101)
            embed2.add_field(
                name="Other Settings",
                value=
                f"To change the punishment type `{ctx.prefix}Antinuke punishment set <type>`\nAvailable Punishments are `Ban`, `Kick` and `None`."
            )
            embed2.set_footer(text=f"Current Punishment Type Is {punish}")
            await ctx.reply(embed=embed2, mention_author=False)

    @_antinuke.command(
        name="recover",
        help="Deletes all channels with name of rules and moderator-only",
        usage="Antinuke recover")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _recover(self, ctx: Context):
        for channel in ctx.guild.channels:
            if channel.name in ('rules', 'moderator-only'):
                try:
                    await channel.delete()
                except:
                    pass
        hacker5 = discord.Embed(
            title="Lock N Loaded",
            description=
            "<a:tick:1072492486674616460> | Successfully Deleted All Channels With Name Of `rules` and `moderator-only`",
            color=0x50101)
        hacker5.set_thumbnail(url=f"{ctx.author.avatar}")
        await ctx.reply(embed=hacker5, mention_author=False)

    @commands.group(
        name="punishment",
        help="Changes Punishment of antinuke and antiraid for this server.",
        invoke_without_command=True,
        usage="Antinuke punishment set/show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _punishment(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_punishment.command(
        name="set",
        help="Changes Punishment of antinuke and automod for this server.",
        aliases=["change"],
        usage="Antinuke punishment set <none>")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_set(self, ctx, punishment: str):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:

            kickOrBan = punishment.lower()

            if kickOrBan == "kick":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "kick"
                hacker = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"<a:tick:1072492486674616460> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=0x50101)
                await ctx.reply(embed=hacker, mention_author=False)

                updateConfig(ctx.guild.id, data)

            elif kickOrBan == "ban":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "ban"
                hacker1 = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"<a:tick:1072492486674616460> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=0x50101)
                await ctx.reply(embed=hacker1, mention_author=False)

                updateConfig(ctx.guild.id, data)

            elif kickOrBan == "none":
                data = getConfig(ctx.guild.id)
                data["punishment"] = "none"
                hacker3 = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"<a:tick:1072492486674616460> | Successfully Changed Punishment To: **{kickOrBan}** For {ctx.guild.name}",
                    color=0x50101)
                await ctx.reply(embed=hacker3, mention_author=False)

                updateConfig(ctx.guild.id, data)
            else:
                hacker6 = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    "Invalid Punishment Type\nValid Punishment Type(s) Are: Kick, Ban, None",
                    color=0x50101)
                await ctx.reply(embed=hacker6, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_punishment.command(name="show",
                         help="Shows custom punishment type for this server",
                         usage="Antinuke punishment show")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def punishment_show(self, ctx: Context):
        data = getConfig(ctx.guild.id)
        punish = data["punishment"]
        hacker5 = discord.Embed(
            color=0x50101,
            title="Lock N Loaded",
            description=
            "Custom punishment of anti-nuke and automod in this server is: **{}**"
            .format(punish.title()))
        await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.command(name="channelclean",
                       aliases=['cc'],
                       help="deletes channel with similar name provided.",
                       usage="Antinuke channelclean <none>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def _channelclean(self, ctx: Context, channeltodelete: str):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            for channel in ctx.message.guild.channels:
                if channel.name == channeltodelete:
                    try:
                        await channel.delete()
                    except:
                        pass
            hacker1 = discord.Embed(
                title="Lock N Loaded",
                description=
                f"<a:tick:1072492486674616460> | Successfully Deleted All Channels With The Name Of {channeltodelete}",
                color=0x50101)
            await ctx.reply(embed=hacker1, mention_author=False)
        elif ctx.author.id == 1031110964898177054:
            for channel in ctx.message.guild.channels:
                if channel.name == channeltodelete:
                    try:
                        await channel.delete()
                    except:
                        pass
            hacker2 = discord.Embed(
                title="Lock N Loaded",
                description=
                f"<a:tick:1072492486674616460> | Successfully Deleted All Channels With The Name Of {channeltodelete}",
                color=0x50101)
            await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_antinuke.command(name="roleclean",
                       aliases=['cr'],
                       help="deletes role with similar name provided",
                       usage="Antinuke roleclean <none>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _roleclean(self, ctx: Context, roletodelete: str):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            for role in ctx.message.guild.roles:
                if role.name == roletodelete:
                    try:
                        await role.delete()
                    except:
                        pass
            hacker = discord.Embed(
                title="Lock N Loaded",
                description=
                f"<a:tick:1072492486674616460> | Successfully Deleted All Roles With The Name Of {roletodelete}",
                color=0x50101)
            await ctx.reply(embed=hacker, mention_author=False)
        elif ctx.author.id == 1031110964898177054:
            for role in ctx.message.guild.roles:
                if role.name == roletodelete:
                    try:
                        await role.delete()
                    except:
                        pass
            hacker3 = discord.Embed(
                title="Lock N Loaded",
                description=
                f"<a:tick:1072492486674616460> | Successfully Deleted All Roles With The Name Of {roletodelete}",
                color=0x50101)
            await ctx.reply(embed=hacker3, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @commands.group(name="whitelist",
                     aliases=["wl"],
                     help="Whitelist your TRUSTED users for anti-nuke",
                     invoke_without_command=True,
                     usage="Antinuke whitelist add/remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _whitelist(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_whitelist.command(name="add",
                        help="Add a user to whitelisted users",
                        usage="Antinuke whitelist add <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_add(self, ctx, user: discord.User):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        owner = ctx.guild.owner
        wlrole = data['wlrole']

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(wled) == 15:
                hacker = discord.Embed(
                    title="Lock N Loaded",
                    description=
                    f"<a:astroz_cross:1072464778313879634> This server have already maximum number of whitelisted users (15)\nRemove one to add another :)",
                    color=0x50101)
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                if str(user.id) in wled:
                    hacker1 = discord.Embed(
                        title="Lock N Loaded",
                        description=
                        f"<a:astroz_cross:1072464778313879634> That user is already in my whitelist.",
                        color=0x50101)
                    await ctx.reply(embed=hacker1, mention_author=False)
                else:
                    wled.append(str(user.id))
                    updateConfig(ctx.guild.id, data)
                    hacker4 = discord.Embed(
                        color=0x50101,
                        title="Lock N Loaded",
                        description=
                        f"<a:tick:1072492486674616460> | Successfully Whitelisted {user.mention} For {ctx.guild.name}"
                    )
                    await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_whitelist.command(name="remove",
                        help="Remove a user from whitelisted users",
                        usage="Antinuke whitelist remove <user>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_remove(self, ctx, user: discord.User):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        wlrole = data['wlrole']
        hacker = ctx.guild.get_member(ctx.author.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if str(user.id) in wled:
                wled.remove(str(user.id))
                updateConfig(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=0x50101,
                    title="Lock N Loaded",
                    description=
                    f"<a:tick:1072492486674616460> | Successfully Unwhitelisted {user.mention} For {ctx.guild.name}"
                )
                await ctx.reply(embed=hacker, mention_author=False)
            else:
                hacker2 = discord.Embed(
                    color=0x50101,
                    title="Lock N Loaded",
                    description=
                    "<a:astroz_cross:1072464778313879634> | That user is not in my whitelist."
                )
                await ctx.reply(embed=hacker2, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_whitelist.command(name="show",
                        help="Shows list of whitelisted users in the server.",
                        usage="Antinuke whitelist show")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_show(self, ctx):
        data = getConfig(ctx.guild.id)
        wled = data["whitelisted"]
        if len(wled) == 0:
            hacker = discord.Embed(
                color=0x50101,
                title="Lock N Loaded",
                description=
                f"<a:astroz_cross:1072464778313879634> | There aren\'t any whitelised users for this server"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            entries = [
                f"`{no}` | <@!{idk}> | ID: [{idk}](https://discord.com/users/{idk})"
                for no, idk in enumerate(wled, start=1)
            ]
            paginator = Paginator(source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Whitelisted Users of {ctx.guild.name} - 15/{len(wled)}",
                description="",
                color=0x2F3136),
                                  ctx=ctx)
            await paginator.paginate()

    @_whitelist.command(name="reset",
                        help="removes every user from whitelist database",
                        aliases=["clear"],
                        usage="Antinuke whitelist reset")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def wl_reset(self, ctx: Context):
        data = getConfig(ctx.guild.id)
        wlrole = data['wlrole']
        hacker = ctx.guild.get_member(ctx.author.id)
        wlroles = ctx.guild.get_role(wlrole)

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data = getConfig(ctx.guild.id)
            data["whitelisted"] = []
            updateConfig(ctx.guild.id, data)
            hacker = discord.Embed(
                color=0x50101,
                title="Lock N Loaded",
                description=
                f"<a:tick:1072492486674616460> | Successfully Cleared Whitelist Database For **{ctx.guild.name}**"
            )
            await ctx.reply(embed=hacker, mention_author=False)
        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)

    @_whitelist.command(name="role",
                        help="Add a role to whitelisted role",
                        usage="Antinuke whitelist role")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist_role(self, ctx, role: discord.Role):
        data = getConfig(ctx.guild.id)
        data["wlrole"] = role.id
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            updateConfig(ctx.guild.id, data)
            hacker4 = discord.Embed(
                color=0x50101,
                title="Lock N Loaded",
                description=
                f"<a:tick:1072492486674616460> | {role.mention} Has Been Added To Whitelisted Role For {ctx.guild.name}"
            )
            await ctx.reply(embed=hacker4, mention_author=False)

        else:
            hacker5 = discord.Embed(
                description=
                """```yaml\n - You must have Administrator permission.\n - Your top role should be above my top role.```""",
                color=0x50101)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")
            await ctx.reply(embed=hacker5, mention_author=False)
