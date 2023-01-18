import logging

from aiohttp import ClientResponseError
from discord import Cog
from leek import LeekBot

LOGGER = logging.getLogger("leek_modding")
NATIVE_LINKS = {
    "gtav": "https://raw.githubusercontent.com/alloc8or/gta5-nativedb-data/master/natives.json",
    "rdr3": "https://raw.githubusercontent.com/alloc8or/rdr3-nativedb-data/master/natives.json",
    "fivem": "https://runtime.fivem.net/doc/natives_cfx.json"
}
NATIVES = {}


class GrandTheftAuto(Cog):
    """
    Grand Theft Auto related commands.
    """
    def __init__(self, bot: LeekBot):
        self.bot: LeekBot = bot

    @Cog.listener()
    async def on_connect(self):
        for game, url in NATIVE_LINKS.items():
            try:
                async with await self.bot.get(url) as resp:
                    resp.raise_for_status()
                    json: dict[str, dict[str, dict[str, str]]] = await resp.json(content_type=None)

                    for namespace, natives in json.items():
                        for n_hash, n_data in natives.items():
                            native = {
                                "namespace": namespace,
                                "hash": n_hash,
                                **n_data
                            }
                            NATIVES[n_hash] = native
            except ClientResponseError as e:
                LOGGER.exception(f"Can't request {url}: Code {e.status}")
            except BaseException:
                LOGGER.exception(f"Unable to get {game} natives from {url}")
