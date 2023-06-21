import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio


class close(Button):
    def __init__(self):
        super().__init__(label=f'Close', emoji='🔒', style=discord.ButtonStyle.grey, custom_id="close")
        self.callback = self.button_callback
    
    async def button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Closing this ticketing in 5 seconds.', ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

class closeTicket(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(close())

class create(Button):
    def __init__(self):
        super().__init__(label='Create ticket', style=discord.ButtonStyle.grey, custom_id=f'create', emoji = '📩')
        self.callback = self.button_callback
    
    async def button_callback(self, interaction: discord.Interaction):
        categ = discord.utils.get(interaction.guild.categories, name='Ticket-category')
        
        for ch in categ.channels:
            if ch.topic == str(interaction.user):
                await interaction.response.send_message("You already have a ticket open.", ephemeral=True)
                return
        overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                }
        channel = await categ.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, topic=f'{interaction.user}')
        await interaction.response.send_message(f">>> Your ticket has been created at {channel.mention}", ephemeral=True)
        embed = discord.Embed(
                    title=f'Ticket',
                    description=f'Thanks for reaching out!\nThe support Team will be here shortly\nPlease be patient.\n\nClick 🔒 to close the ticket.',
                    color = 0x50101
                )
        await channel.send(f'{interaction.user.mention} Welcome', embed=embed, view=closeTicket())

class createTicket(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(create())

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    


  
    @commands.group(name="Ticket", description="Ticket Setup")
    async def ticket(self, ctx: commands.Context):
        ...
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def sendpanel(self, ctx: commands.Context):
        embed = discord.Embed(title=f'Ticket', description=f'>>> To create a ticket click the 📩 button.', color=0x50101)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f'{self.bot.user.name} - Ticketing without clutter')
        guild = ctx.guild       
        await guild.create_category_channel(name="Ticket-category")
        await ctx.send(embed=embed, view=createTicket())


