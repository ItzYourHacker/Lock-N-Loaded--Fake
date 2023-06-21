from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Dict, Optional
import discord
from discord.ext import commands
from discord.ext import menus
from discord.ext.commands import Context
from discord import Interaction, ButtonStyle


class Paginator(discord.ui.View):

    def __init__(
        self,
        source: menus.PageSource,
        *,
        ctx: Context | Interaction,
        check_embeds: bool = True,
    ):
        super().__init__()
        self.source: menus.PageSource = source
        self.check_embeds: bool = check_embeds
        self.ctx = ctx
        self.message: Optional[discord.Message] = None
        self.current_page: int = 0
        self.clear_items()
        self.fill_items()

    def fill_items(self) -> None:

        if self.source.is_paginating():
            max_pages = self.source.get_max_pages()
            use_last_and_first = max_pages is not None and max_pages >= 2
            if use_last_and_first:
                self.add_item(self.first_page_button)
            self.add_item(self.previous_page_button)
            self.add_item(self.stop_button)
            self.add_item(self.next_page_button)
            if use_last_and_first:
                self.add_item(self.last_page_button)
                self.add_item(self.stop_button)

    async def _get_kwargs_from_page(self, page: int) -> Dict[str, Any]:
        value = await discord.utils.maybe_coroutine(self.source.format_page,
                                                    self, page)
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return {'content': value, 'embed': None}
        elif isinstance(value, discord.Embed):
            return {'embed': value, 'content': None}
        else:
            return {}

    async def show_page(self, interaction: discord.Interaction,
                        page_number: int) -> None:
        page = await self.source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(page_number)
        if kwargs:
            if interaction.response.is_done():
                if self.message:
                    await self.message.edit(**kwargs, view=self)
            else:
                await interaction.response.edit_message(**kwargs, view=self)

    def _update_labels(self, page_number: int) -> None:
        self.first_page_button.disabled = page_number == 0
        self.next_page_button.disabled = False
        self.previous_page_button.disabled = False

        max_pages = self.source.get_max_pages()
        if max_pages is not None:
            self.last_page_button.disabled = (page_number + 1) >= max_pages
            if (page_number + 1) >= max_pages:
                self.next_page_button.disabled = True
            if page_number == 0:
                self.previous_page_button.disabled = True

    async def show_checked_page(self, interaction: discord.Interaction,
                                page_number: int) -> None:
        max_pages = self.source.get_max_pages()
        try:
            if max_pages is None:
                await self.show_page(interaction, page_number)
            elif max_pages > page_number >= 0:
                await self.show_page(interaction, page_number)
        except IndexError:
            pass

    async def interaction_check(self,
                                interaction: discord.Interaction) -> bool:
        if isinstance(self.ctx, Interaction):
            if interaction.user and interaction.user.id in (
                    self.ctx.client.owner_id, self.ctx.user.id):
                return True
            await interaction.response.send_message(
                'This pagination menu cannot be controlled by you, sorry!',
                ephemeral=True)
            return False
        if interaction.user and interaction.user.id in (self.ctx.bot.owner_id,
                                                        self.ctx.author.id):
            return True
        await interaction.response.send_message(
            'This pagination menu cannot be controlled by you, sorry!',
            ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        if self.message:
            await self.message.edit(view=None)

    async def on_error(self, interaction: discord.Interaction,
                       error: Exception, item: discord.ui.Item) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry',
                                            ephemeral=True)
        else:
            await interaction.response.send_message(
                'An unknown error occurred, sorry', ephemeral=True)

    def update_styles(self, **kwargs):
        """
        Update the button styles and emojis
        """

        
        self.first_page_button.label = kwargs.get('first_button_emoji') or '≪'
        self.previous_page_button.label = kwargs.get(
            'previous_button_emoji') or 'Back'
        self.next_page_button.label = kwargs.get('next_button_emoji') or 'Next'
        self.last_page_button.label = kwargs.get('last_button_emoji') or '≫'
        self.stop_button.emoji = kwargs.get(
            'stop_button_emoji') or '<a:astroz_cross:1072464778313879634>'

        
        self.first_page_button.style = kwargs.get(
            'first_button_style') or ButtonStyle.blurple
        self.previous_page_button.style = kwargs.get(
            'previous_button_style') or ButtonStyle.success
        self.stop_button.style = kwargs.get(
            'stop_button_style') or ButtonStyle.red
        self.next_page_button.style = kwargs.get(
            'next_button_style') or ButtonStyle.success
        self.last_page_button.style = kwargs.get(
            'last_button_style') or ButtonStyle.blurple

    async def paginate(self,
                       *,
                       content: Optional[str] = None,
                       ephemeral: bool = False,
                       **kwargs) -> None:
        self.update_styles(**kwargs)
        if isinstance(self.ctx, Interaction):
            await self.source._prepare_once()
            page = await self.source.get_page(0)
            kwargs = await self._get_kwargs_from_page(page)
            if content:
                kwargs.setdefault('content', content)
            self._update_labels(0)
            self.message = await self.ctx.response.send_message(
                **kwargs, view=self, ephemeral=ephemeral)
            return

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        if content:
            kwargs.setdefault('content', content)
        self._update_labels(0)
        self.message = await self.ctx.send(**kwargs,
                                           view=self,
                                           ephemeral=ephemeral)

    @discord.ui.button()
    async def first_page_button(self, interaction: discord.Interaction,
                                button: discord.ui.Button):
        """Go to the first page"""
        await self.show_page(interaction, 0)

    @discord.ui.button()
    async def previous_page_button(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
        """Go to the previous page"""
        await self.show_checked_page(interaction, self.current_page - 1)

    @discord.ui.button()
    async def stop_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        """Stops the pagination session."""
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()

    @discord.ui.button()
    async def next_page_button(self, interaction: discord.Interaction,
                               button: discord.ui.Button):
        """Go to the next page"""
        await self.show_checked_page(interaction, self.current_page + 1)

    @discord.ui.button()
    async def last_page_button(self, interaction: discord.Interaction,
                               button: discord.ui.Button):
        """Go to the last page"""
        await self.show_page(interaction, self.source.get_max_pages() - 1)
