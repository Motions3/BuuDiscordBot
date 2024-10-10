import random
import discord
from discord.ext import commands
import sqlite3
import os

class LevelingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = './databases/levels.db'
        self.create_or_load_database()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    def create_or_load_database(self):
        db_exists = os.path.exists(self.db_path)
        self.db = sqlite3.connect(self.db_path)
        if not db_exists:
            self.create_tables()

    def create_tables(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            level INTEGER DEFAULT 0,
            total_xp INTEGER DEFAULT 0,
            next_level INTEGER DEFAULT 100
        )''')
        self.db.commit()
        print("Database and tables created successfully.")

    def get_user_data(self, user_id):
        cur = self.db.execute("SELECT level, total_xp, next_level FROM users WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if result:
            return {"level": result[0], "total_xp": result[1], "next_level": result[2]}
        else:
            self.db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            self.db.commit()
            return {"level": 0, "total_xp": 0, "next_level": 100}

    def update_user_data(self, user_id, total_xp, level, next_level):
        self.db.execute("UPDATE users SET total_xp = ?, level = ?, next_level = ? WHERE user_id = ?",
                        (total_xp, level, next_level, user_id))
        self.db.commit()

    def calculate_next_level_xp(self, level):
        """
        Calculate how much XP is needed to reach the next level.
        Each level requires an additional 100 * level XP.
        """
        return (level + 1) * 100

    def update_user_experience(self, user_id, exp):
        """
        Update the user's experience and level if applicable.
        """
        user_data = self.get_user_data(user_id)
        total_xp = user_data["total_xp"] + exp
        level = user_data["level"]
        next_level_xp = user_data["next_level"]

        # Level up as long as the total XP exceeds the XP needed for the next level
        leveled_up = False
        while total_xp >= next_level_xp:
            level += 1
            total_xp -= next_level_xp
            next_level_xp = self.calculate_next_level_xp(level)
            leveled_up = True

        # Update user data in the database
        self.update_user_data(user_id, total_xp, level, next_level_xp)

        if leveled_up:
            return level
        else:
            return None

    async def award_gold(self, user_id, amount):
        """
        Optional function to award gold (can be linked to another cog).
        """
        currency_cog = self.bot.get_cog('Currency')
        if currency_cog:
            currency_cog.update_gold(user_id, amount)
        else:
            print("Currency cog not found. Unable to award gold.")

    @commands.command()
    async def profile(self, ctx):
        """
        Display the user's current level, total experience, and XP needed for the next level.
        """
        user_data = self.get_user_data(ctx.author.id)
        await ctx.send(
            f"Your level: {user_data['level']}\n"
            f"Your total experience: {user_data['total_xp']}\n"
            f"XP needed for next level: {user_data['next_level'] - user_data['total_xp']}"
        )

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        """
        Display the level and XP of the mentioned user or the command invoker if no user is mentioned.
        """
        if member is None:
            member = ctx.author

        user_data = self.get_user_data(member.id)
        await ctx.send(
            f"{member.mention}'s level: {user_data['level']}\n"
            f"Total experience: {user_data['total_xp']}\n"
            f"XP needed for next level: {user_data['next_level'] - user_data['total_xp']}"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Award random XP between 5-15 for each message sent by a user, except bot messages.
        If the user levels up, notify the channel and award gold.
        """
        if message.author.bot:
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        user_id = message.author.id
        gained_exp = random.randint(5, 15)
        new_level = self.update_user_experience(user_id, gained_exp)

        if new_level:
            await message.channel.send(f"{message.author.mention} leveled up to level {new_level}!")
            await self.award_gold(user_id, 1000)  # Optional: award gold on level-up

async def setup(bot):
    await bot.add_cog(LevelingCog(bot))