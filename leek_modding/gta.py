import logging
import string

from aiohttp import ClientResponseError
from discord import Cog, ApplicationContext, slash_command, Option, AutocompleteContext, Embed
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


def format_params(params: dict):
    if params is None:
        return ""

    formatted = "\n    "

    for param in params:
        type = param["type"]
        name = param["name"]
        description = param.get("description", None)

        formatted += "`{0}: {1}`".format(name, type)

        if description:
            formatted += " {0}\n".format(description)
        else:
            formatted += "\n"

    return formatted


def find_native(name: str, game: str):
    natives = NATIVES.get(game, None)

    if natives is None:
        return None

    return next((x for x in natives if x["hash"] == name or x["name"] == name), None)


async def get_natives(ctx: AutocompleteContext):
    natives = NATIVES["gtav"]
    return list(x["name"] for x in natives)


async def get_games(ctx: AutocompleteContext):
    return list(NATIVES.keys())


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

    @slash_command()
    async def native(self, ctx: ApplicationContext, name: Option(str, "The name to search", autocomplete=get_natives),
                     game: Option(str, "The game for this native", default="gtav", autocomplete=get_games)):
        found = find_native(name, game)

        if found is None:
            await ctx.respond("The native was not found!", ephemeral=True)
            return

        params = format_params(found["params"])

        embed = Embed()
        embed.title = found["name"]
        embed.description = "**Hash**: {0}\n**Lua Name**: {1}\n**Parameters**: {2}".format(found["hash"],
                                                                                           found["lua"],
                                                                                           params)

        await ctx.respond(embed=embed)
