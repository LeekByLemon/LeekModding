from discord import Cog
from leek import LeekBot


class GrandTheftAuto(Cog):
    """
    Grand Theft Auto related commands.
    """
    def __init__(self, bot: LeekBot):
        self.bot: LeekBot = bot
