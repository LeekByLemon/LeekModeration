import asyncio
import logging
from typing import Union

from discord import Cog, Message, Member, User, slash_command, Forbidden, NotFound, HTTPException, ApplicationContext
from leek import LeekBot, get_default, localize

LOGGER = logging.getLogger("leek_moderation")


class Moderation(Cog):
    """
    Set of tools for the Moderation of Discord servers.
    """
    def __init__(self, bot: LeekBot):
        self.bot: LeekBot = bot

    def make_check(self, original: Message, check: Union[Member, User]):
        def func(msg: Message):
            return msg.author == check and original != msg

        return func

    async def safely_delete(self, ctx: ApplicationContext, message: Message):
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
                return

            await ctx.send(localize("MODERATION_COMMAND_CLEAR_LIMIT_LOCAL", ctx.locale, retry),
                           delete_after=10)
            await asyncio.sleep(retry + 1)
            return await self.safely_delete(ctx, message)

    @slash_command(name=get_default("MODERATION_COMMAND_CLEAR_NAME"),
                   description=get_default("MODERATION_COMMAND_CLEAR_HELP"))
    async def clear(self, ctx: ApplicationContext, keep: Member):
        await ctx.defer(ephemeral=True)

        matches = self.make_check(ctx.message, keep)

        async for message in ctx.channel.history(limit=100):
            if matches(message):
                continue
            await self.safely_delete(ctx, message)

        await ctx.followup.send(localize("MODERATION_COMMAND_CLEAR_DONE", ctx.locale), ephemeral=True)
