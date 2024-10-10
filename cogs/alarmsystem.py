import discord
from discord.ext import commands, tasks
import asyncio


class AlarmCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_alarms = {}

    @commands.command()
    async def alarm(self, ctx, minutes: int):
        if minutes <= 0:
            await ctx.send("Please provide a positive number of minutes.")
            return

        user_id = ctx.author.id
        if user_id in self.active_alarms:
            await ctx.send("You already have an active alarm. Please wait for it to finish or cancel it.")
            return

        await ctx.send(f"Alarm set for {minutes} minutes.")
        self.active_alarms[user_id] = asyncio.create_task(self.run_alarm(ctx.author, minutes))

    async def run_alarm(self, user, minutes):
        await asyncio.sleep(minutes * 60)

        while user.id in self.active_alarms:
            try:
                await user.send(f"@{user.name}, Timer Up! Type 'Stop' To Cancel Alarm")

                def check(m):
                    return m.author == user and m.channel == user.dm_channel and m.content.lower() == 'stop'

                await self.bot.wait_for('message', check=check, timeout=2)
                del self.active_alarms[user.id]
                await user.send("Alarm stopped.")
            except asyncio.TimeoutError:
                pass  # If 2 seconds pass without 'stop', we'll send the message again

    def cog_unload(self):
        for task in self.active_alarms.values():
            task.cancel()


async def setup(bot):
    await bot.add_cog(AlarmCog(bot))