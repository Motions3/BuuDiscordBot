import os
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle

# Environment Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot Startup
bot = commands.Bot(command_prefix="..", intents=discord.Intents.all())

# Bot status, loops from 1-3
status_cycle = cycle(["BUU HAVING FUN!", "BUU HUNGRY!!!", "BUU GO SLEEP NOW!"])


# Bot Change Status In Seconds - 86400 = 24hours
@tasks.loop(seconds=86400)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))


# Bot Ready Check
@bot.event
async def on_ready():
    print("BUU is now online!")
    change_bot_status.start()  # Starts the status loop


# Load bot functions/cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


asyncio.run(main())
