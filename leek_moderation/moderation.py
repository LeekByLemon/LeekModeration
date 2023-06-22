import logging

from discord import Cog
from leek import LeekBot

LOGGER = logging.getLogger("leek_moderation")


class Moderation(Cog):
    """
    Set of tools for the Moderation of Discord servers.
    """
    def __init__(self, bot: LeekBot):
        self.bot: LeekBot = bot
