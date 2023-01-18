import logging
import string

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


def format_lua_name(name: str):
    return string.capwords(name.lower().replace("0x", "N_0x").replace("_", " ")).replace(" ", "")


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
                    ready = []

                    for namespace, natives in json.items():
                        for n_hash, n_data in natives.items():
                            name = n_data["name"]
                            native = {
                                "namespace": namespace,
                                "hash": n_hash,
                                "lua": format_lua_name(name),
                                **n_data
                            }

                            if n_hash in NATIVES:
                                LOGGER.warning(f"Found Duplicated Native: {n_hash}/{name}")

                            ready.append(native)

                    NATIVES[game] = ready
            except ClientResponseError as e:
                LOGGER.exception(f"Can't request {url}: Code {e.status}")
            except BaseException:
                LOGGER.exception(f"Unable to get {game} natives from {url}")

        LOGGER.info("Finished fetching the natives")
