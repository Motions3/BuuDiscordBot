import os
import discord

from random import randint, choice, uniform, seed
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = int(os.getenv('OWNER'))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    # Start of Bot Commands -------------------------------------------------------------------------------------------

    # Owner Shutdown Command - Shuts down the bot if the user is the owner
    @commands.command()
    async def shutdown(self, ctx):
        print(f"User ID calling shutdown: {ctx.author.id}")
        print(f"Owner ID: {self.owner_id}")

        if ctx.author.id == self.owner_id:
            embed = discord.Embed(
                title="Shutting Down...",
                description=f"Goodbye, {ctx.author.mention}!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            await self.bot.close()

    # Hello Command - Used for testing
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello there, {ctx.author.mention}")

    # Roll Command
    @commands.command()
    async def roll(self, ctx, diceroll: int):
        """Rolls a die with the given number of sides (dice roll)."""

        if diceroll <= 0:
            embed = discord.Embed(
                title="Invalid Dice Size",
                description=f"{ctx.author.mention}, please choose a valid number of sides for the dice.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Simulate the dice roll
        dice = randint(1, diceroll)

        # Create an embed for the result
        embed = discord.Embed(
            title="🎲 Dice Roll!",
            description=f"{ctx.author.mention} rolled a {dice} from a d{diceroll}",
            color=discord.Color.green()
        )

        # Send the embed
        await ctx.send(embed=embed)

    # Error handling for roll command
    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            # If user didn't provide an argument
            embed = discord.Embed(
                title="Missing Argument",
                description=f"{ctx.author.mention}, you must use the command like this: `roll <integer>`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            # If user provided something that's not an integer
            embed = discord.Embed(
                title="Invalid Input",
                description=f"{ctx.author.mention}, please provide a valid number. Example: `roll 6`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            # For any other errors
            embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention}, something went wrong. Please try again.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    # F for respect
    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{choice(hearts)}")

    # Reverse text
    @commands.command()
    async def reverse(self, ctx, *, text: str):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    # Coin flip
    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(
            f"**{ctx.author.name}** flipped a coin and got **{choice(coinsides)}**!"
        )

    # Rate anything
    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = uniform(0.0, 100.0)
        await ctx.send(
            f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    # How hot is someone
    @commands.command(aliases=['howhotis', 'hot'])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        seed(user.id)
        r = randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    # Slot machine
    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = choice(emojis)
        b = choice(emojis)
        c = choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} Two in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    # End of Bot Commands ----------------------------------------------------------------------------------------------


async def setup(bot):
    await bot.add_cog(BotCommands(bot))
