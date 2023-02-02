import re

from discord import Cog, ApplicationContext, message_command, Message, Embed
from leek import LeekBot, get_default


RE_SHVDN = re.compile("\[[0-9]{2}:[0-9]{2}:[0-9]{2}] \[(WARNING|ERROR)] (.*)")
RE_INSTANCE = re.compile("A script tried to use a custom script instance of type ([A-Za-z0-9.]*) that was not "
                         "instantiated by ScriptHookVDotNet.")
RE_DEPENDENCY = re.compile("Failed to instantiate script ([A-z0-9_.]*) because constructor threw an exception: "
                           "System.IO.FileNotFoundException: .* '([A-Za-z0-9.]*), Version=([0-9.]*),")
MATCHES = {
    "Failed to load config: System.IO.FileNotFoundException": "The configuration file for SHVDN does not exists",
    RE_INSTANCE: "{0} Mod {1} was not instantiated by SHVDN",
    RE_DEPENDENCY: "{0} {1} requires {2} version {3} or higher but is not installed"
}


class Diagnoser(Cog):
    def __init__(self, bot: LeekBot):
        self.bot = bot

    @message_command(name=get_default("MODDING_MESSAGE_DIAGNOSE_NAME"))
    async def diagnose(self, ctx: ApplicationContext, message: Message):
        if not message.attachments:
            await ctx.respond("There are no log files attached to this message.")
            return

        attachment = message.attachments[0]

        if not attachment.content_type.startswith("text/plain"):
            await ctx.respond("The attachment is not a text file.")
            return

        async with await self.bot.get(attachment.url) as response:
            if not response.ok:
                await ctx.respond(f"Couldn't fetch log file: Code {response.status}")
                return

            content = await response.text()
            lines = content.splitlines()

        problems = []

        for line in lines:
            match = RE_SHVDN.search(line)

            if match is None:
                continue

            level, details = match.groups()
            emoji = "🔴" if level == "ERROR" else "🟡"

            for match, text in MATCHES.items():
                if isinstance(match, re.Pattern):
                    matches = match.match(details)

                    if matches is None:
                        continue

                    message = text.format(emoji, *matches.groups())
                elif isinstance(match, str):
                    if not details.startswith(match):
                        continue

                    message = f"{emoji} {text}"
                else:
                    continue

                if message not in problems:
                    problems.append(message)

        if not problems:
            await ctx.respond("Couldn't detect any issues with the log file.")
        else:
            embed = Embed()
            embed.title = f"Found {len(problems)} problems"
            embed.description = "\n".join(problems)
            await ctx.respond(embed=embed)
