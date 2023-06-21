import discord
import json
from discord.ext import commands
from discord.ui import Button, View


class Verification(commands.Cog):
  def __init__(self, client):
        self.client = client

  @commands.Cog.listener()
  async def on_interaction(self, interaction):
    with open("verification.json", "r") as f:
      data = json.load(f)
    if str(interaction.message.guild.id) not in data:
      return
    elif interaction.data["custom_id"] != "Verify":
      return
    else:
      if interaction.message.guild.get_role(int(data[str(interaction.message.guild.id)]["role"])) in interaction.user.roles:
        return await interaction.response.send_message(content="You are already verified!", ephemeral=True)
      else:
        try:
          await interaction.user.add_roles(interaction.message.guild.get_role(int(data[str(interaction.message.guild.id)]["role"])))
          await interaction.response.send_message(content="You are now officially verified in this server!", ephemeral=True)
        except Exception as e:
          await interaction.response.send_message(content=f"Oops! There was something wrong while adding role. | {e}", ephemeral=True)
  @commands.hybrid_group(name="verification", description="...")
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _verify(self, ctx):
    if ctx.subcommand_passed is None:
        await ctx.send_help(ctx.command)
        ctx.command.reset_cooldown(ctx)

  @_verify.command(name="enable", description="Enable verification in the server.")
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def verify_enable(self, ctx, channel: discord.TextChannel, role: discord.Role):
    with open('verification.json', 'r') as f:
      data = json.load(f)
    if str(ctx.guild.id) in data:
      await ctx.send("Verification is already enabled in this server! first disable it using `verification disable` command and then try again")
    else:
      idk = await ctx.send(embed=discord.Embed(title="Verification", description="Setting Up Verification, Be Patient"))
      btn = Button(style=discord.ButtonStyle.grey, label="", emoji="<a:tick:1072492486674616460>", custom_id="Verify")
      view = View()
      view.add_item(btn)
      embed = discord.Embed(title='Verification', description=f"To Access In {ctx.guild.name} Press the <a:tick:1072492486674616460> Button Below", color=0x2f3136)
      lame = await channel.send(embed=embed, view=view)
      await idk.delete()
      await ctx.send("Successfully Completed Verification Setup!")
      data[str(ctx.guild.id)] = {
        'role': str(role.id),
        'msg': lame.id,
        'channel': channel.id
      }
      with open("verification.json", "w") as f:
        json.dump(data, f, indent=4)

  @_verify.command(name="disable", description="Disable verification in the server.")
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def verify_disable(self, ctx):
    with open("verification.json", 'r') as f:
      data = json.load(f)
    if str(ctx.guild.id) not in data:
      await ctx.send("Verification isn't enabled in this server!")
    else:
      msg = data[str(ctx.guild.id)]["msg"]
      lame = await ctx.fetch_message(int(msg))
      del data[str(ctx.guild.id)]
      try:
        await lame.delete()
      except:
        pass
      with open("verification.json", "w") as f:
        json.dump(data, f, indent=4)
      await ctx.send("Successfully Deleted Verification System In This Guild!")

  @_verify.command(name="config", description="Shows Configuration for verification in this guild.")
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def verify_config(self, ctx):
    with open("verification.json", "r") as f:
      data = json.load(f)
    embed = discord.Embed(title="Verification Configuration", color=0x2f3136)
    embed.add_field(name="Verification Enabled?", value="True" if str(ctx.guild.id) in data else "False", inline=False)
    if str(ctx.guild.id) in data:
      chan = data[str(ctx.guild.id)]["channel"]
      role = int(data[str(ctx.guild.id)]["role"])
      embed.add_field(name="Channel", value=f"<#{chan}>", inline=False)
      embed.add_field(name="Role", value=f"<@&{role}>", inline=False)

    await ctx.send(embed=embed)