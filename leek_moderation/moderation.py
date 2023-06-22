"""
Moderation tools for the Leek bot.
"""

import asyncio
import logging
from typing import Callable, Union

from discord import ApplicationContext, Cog, Forbidden, HTTPException, Member, Message, NotFound, User, slash_command
from leek import LeekBot, get_default, localize

LOGGER = logging.getLogger("leek_moderation")


class Moderation(Cog):
    """
    Set of tools for the Moderation of Discord servers.
    """
    def __init__(self, bot: LeekBot):
        """
        Creates a new moderation cog.
        :param bot: The bot instance to use.
        """
        self.bot: LeekBot = bot

    def _make_check(self, original: Message, check: Union[Member, User]) -> Callable[[Message], bool]:
        def func(msg: Message):  # noqa: ANN202
            return msg.author == check and original != msg

        return func

    async def _safely_delete(self, ctx: ApplicationContext, message: Message) -> bool:
        try:
            await message.delete(reason=f"Clear by {ctx.user} ({ctx.user})")
            return True
        except Forbidden:
            await ctx.send(localize("MODERATION_COMMAND_CLEAR_NO_PERMS", ctx.locale))
            return False
        except NotFound:
            return True
        except HTTPException as e:
            if e.code != 429:
                await ctx.send(localize("MODERATION_COMMAND_CLEAR_HTTP_ERROR", ctx.locale, e.code))
                return False

            response = await e.response.json()
            retry = response["retry_after"]

            if response["global"]:
                await ctx.send(localize("MODERATION_COMMAND_CLEAR_LIMIT_GLOBAL", ctx.locale, retry))
                return False

            await ctx.send(localize("MODERATION_COMMAND_CLEAR_LIMIT_LOCAL", ctx.locale, retry),
                           delete_after=10)
            await asyncio.sleep(retry + 1)
            return await self._safely_delete(ctx, message)

    @slash_command(name=get_default("MODERATION_COMMAND_CLEAR_NAME"),
                   description=get_default("MODERATION_COMMAND_CLEAR_HELP"))
    async def clear(self, ctx: ApplicationContext, keep: Member) -> None:
        """
        Clears the messages of a channel.
        :param ctx: The context of the application.
        :param keep: The member whose messages should stay.
        """
        await ctx.defer(ephemeral=True)

        matches = self._make_check(ctx.message, keep)

        async for message in ctx.channel.history(limit=100):
            if matches(message):
                continue
            await self._safely_delete(ctx, message)

        await ctx.followup.send(localize("MODERATION_COMMAND_CLEAR_DONE", ctx.locale), ephemeral=True)
