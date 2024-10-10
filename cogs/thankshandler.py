import discord
import sqlite3

from discord.ext import commands


class ThanksHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('./databases/thanks.db')
        self.cursor = self.conn.cursor()
        self.create_thanks_db()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    def create_thanks_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS thanks_received
            (guild_id INTEGER, user_id INTEGER, thanks_received INTEGER,
            PRIMARY KEY (guild_id, user_id))
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS thanks_given
            (guild_id INTEGER, user_id INTEGER, thanks_given INTEGER,
            PRIMARY KEY (guild_id, user_id))
        ''')
        self.conn.commit()

    @commands.command()
    async def thanks(self, ctx, member: discord.Member):
        if member == ctx.author:
            await ctx.send("You can't thank yourself!")
            return

        guild_id = ctx.guild.id
        thanked_user_id = member.id
        thanking_user_id = ctx.author.id

        self.cursor.execute('''
            INSERT OR REPLACE INTO thanks_received (guild_id, user_id, thanks_received)
            VALUES (?, ?, COALESCE((SELECT thanks_received FROM thanks_received
            WHERE guild_id = ? AND user_id = ?), 0) + 1)
        ''', (guild_id, thanked_user_id, guild_id, thanked_user_id))

        self.cursor.execute('''
            INSERT OR REPLACE INTO thanks_given (guild_id, user_id, thanks_given)
            VALUES (?, ?, COALESCE((SELECT thanks_given FROM thanks_given
            WHERE guild_id = ? AND user_id = ?), 0) + 1)
        ''', (guild_id, thanking_user_id, guild_id, thanking_user_id))

        self.conn.commit()

        await ctx.send(f"{member.mention} has been thanked!")

    @commands.command()
    async def rep(self, ctx, member: discord.Member):
        guild_id = ctx.guild.id
        user_id = member.id

        # Get thanks received
        self.cursor.execute('''
            SELECT thanks_received FROM thanks_received
            WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))
        thanks_received_result = self.cursor.fetchone()
        thanks_received = thanks_received_result[0] if thanks_received_result else 0

        # Get thanks given
        self.cursor.execute('''
            SELECT thanks_given FROM thanks_given
            WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))
        thanks_given_result = self.cursor.fetchone()
        thanks_given = thanks_given_result[0] if thanks_given_result else 0

        await ctx.send(
            f"{member.mention}'s Reputation:\nThanks Received: {thanks_received}\nThanks Given: {thanks_given}")

    def cog_unload(self):
        self.conn.close()


async def setup(bot):
    await bot.add_cog(ThanksHandler(bot))
