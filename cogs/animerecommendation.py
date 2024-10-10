import discord
import aiohttp
import random

from discord.ext import commands

# Jikan API base URL
JIKAN_API_URL = "https://api.jikan.moe/v4"

# List of available genres to choose from (add more if needed)
GENRES = {
    "Action": 1,
    "Adventure": 2,
    "Comedy": 4,
    "Drama": 8,
    "Fantasy": 10,
    "Horror": 14,
    "Romance": 22,
    "Sci-Fi": 24,
    "Slice of Life": 36,
}

class AnimeRecommendationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    # Command to start the recommendation process
    @commands.command(name="recanime")
    async def recanime(self, ctx):
        # Step 1: Prompt user for a genre with an embed
        genre_message = "Please choose a genre from the following:"
        embed = discord.Embed(title=genre_message, color=discord.Color.blue())
        embed.add_field(name="Available Genres", value="\n".join([f"- {genre}" for genre in GENRES.keys()]), inline=False)
        await ctx.send(embed=embed)

        # Wait for the user's response
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            # Wait for genre input
            genre_msg = await self.bot.wait_for("message", check=check, timeout=30)
            genre_choice = genre_msg.content.title()  # Convert input to title case
        except TimeoutError:
            return await ctx.send("Sorry, you took too long to respond. Please try again.")

        # Step 2: Check if the genre is valid (case insensitive)
        if genre_choice not in GENRES:
            return await ctx.send("Invalid genre selected. Please choose a valid genre.")

        # Fetch random anime based on genre
        genre_id = GENRES[genre_choice]
        anime = await self.fetch_random_anime(genre_id)

        # Step 3: Send anime recommendation
        if anime:
            embed = discord.Embed(
                title=anime['title'],
                url=anime['url'],
                description=anime.get('synopsis', 'No synopsis available.'),
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=anime['images']['jpg']['image_url'])
            embed.add_field(name="Score", value=anime.get('score', 'N/A'), inline=True)
            embed.add_field(name="Episodes", value=anime.get('episodes', 'N/A'), inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't find an anime for that genre. Please try again later.")

    # Function to fetch random anime from the Jikan API
    async def fetch_random_anime(self, genre_id):
        try:
            async with aiohttp.ClientSession() as session:
                # Updated URL with limit set to 25
                url = f"{JIKAN_API_URL}/anime?genres={genre_id}&order_by=score&sort=desc&page=1&limit=25"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        animes = data.get('data', [])
                        if animes:
                            return random.choice(animes)  # Choose a random anime
                    else:
                        print(f"Error: received status code {response.status}")
        except Exception as e:
            print(f"Error fetching anime: {e}")
        return None

# Setup function to add this cog to the bot
async def setup(bot):
    await bot.add_cog(AnimeRecommendationCog(bot))
