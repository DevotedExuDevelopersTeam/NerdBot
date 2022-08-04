import os
import re

import aiosqlite
import disnake
from disnake.ext import commands
from exencolorlogs import Logger


REPLACEMENTS = [
    ("is", "isn't"),
    ("are", "aren't"),
    ("am", "ain't"),
    ("do", "don't"),
    ("does", "doesn't"),
    ("was", "wasn't"),
]


class Bot(commands.Bot):
    con: aiosqlite.Connection

    def __init__(self):
        intents = disnake.Intents.default()
        intents.message_content = True
        super().__init__(
            "nerd", strip_after_prefix=True, case_insensitive=True, intents=intents
        )
        self.log = Logger()

    async def on_ready(self):
        self.log.ok("Bot is ready lmao")


bot = Bot()


@bot.listen()
async def on_message(msg: disnake.Message):
    if msg.author.bot or msg.channel.id != 1004750801408893130:
        return
    content = msg.content.lower().split()
    output = ["Um, actually,"]
    is_modified = False
    for word in content:
        w = word
        for w1, w2 in REPLACEMENTS:
            if word == w1:
                w = w2
                is_modified = True
                break
            elif word == w2:
                w = w1
                is_modified = True
                break
        output.append(w)

    s = " ".join(output)
    s = (
        s.replace("you aren", "I ain")
        .replace("you are", "I am")
        .replace("yours", "mine")
        .replace("you", "I")
    )
    for mt in re.findall(f"<@!?{bot.user.id}>", s):
        s = s.replace(mt, "")
    if is_modified:
        await msg.reply(s)


bot.run(os.environ["TOKEN"])
