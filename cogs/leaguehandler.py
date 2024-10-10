import discord
import requests
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class LeagueHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv('RIOT_API_KEY')
        self.base_url = "https://{}.api.riotgames.com"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    @commands.command()
    async def lolrank(self, ctx, game_name: str, tag_line: str, region: str):
        try:
            rank_data = await self.fetch_rank_data(game_name, tag_line, region)

            random_color = discord.Color(random.randint(0, 0xFFFFFF))

            embed = discord.Embed(title=f"League of Legend Rank Checker", color=random_color)
            embed.add_field(name="Summoner Name", value=f"{game_name}#{tag_line}", inline=False)
            embed.add_field(name="Region", value=region.upper(), inline=False)
            embed.add_field(name="Rank", value=rank_data['rank'], inline=False)
            embed.add_field(name="Wins", value=rank_data['wins'], inline=True)
            embed.add_field(name="Losses", value=rank_data['losses'], inline=True)
            embed.add_field(name="Win Rate", value=f"{rank_data['win_rate']}%", inline=False)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    async def fetch_rank_data(self, game_name, tag_line, region):
        region_route = self.get_region_route(region)

        # Get account data
        account_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        account_response = requests.get(account_url, headers={"X-Riot-Token": self.api_key})
        account_response.raise_for_status()
        account_data = account_response.json()

        # Get summoner data
        summoner_url = f"{self.base_url.format(region_route)}/lol/summoner/v4/summoners/by-puuid/{account_data['puuid']}"
        summoner_response = requests.get(summoner_url, headers={"X-Riot-Token": self.api_key})
        summoner_response.raise_for_status()
        summoner_data = summoner_response.json()

        # Get rank data
        rank_url = f"{self.base_url.format(region_route)}/lol/league/v4/entries/by-summoner/{summoner_data['id']}"
        rank_response = requests.get(rank_url, headers={"X-Riot-Token": self.api_key})
        rank_response.raise_for_status()
        rank_data = rank_response.json()

        # Process rank data
        solo_queue_data = next((queue for queue in rank_data if queue['queueType'] == 'RANKED_SOLO_5x5'), None)

        if solo_queue_data:
            wins = solo_queue_data['wins']
            losses = solo_queue_data['losses']
            total_games = wins + losses
            win_rate = round((wins / total_games) * 100, 2) if total_games > 0 else 0
            rank = f"{solo_queue_data['tier']} {solo_queue_data['rank']}"
        else:
            wins, losses, win_rate = 0, 0, 0
            rank = "Unranked"

        return {
            'rank': rank,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate
        }

    def get_region_route(self, region):
        region_routes = {
            'na': 'na1', 'euw': 'euw1', 'eune': 'eun1', 'kr': 'kr',
            'br': 'br1', 'jp': 'jp1', 'ru': 'ru', 'oce': 'oc1',
            'tr': 'tr1', 'lan': 'la1', 'las': 'la2'
        }
        return region_routes.get(region.lower(), 'euw')  # Default to NA if unknown


async def setup(bot):
    await bot.add_cog(LeagueHandler(bot))