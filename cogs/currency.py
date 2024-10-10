import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import random
import sqlite3
import csv
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio

load_dotenv()

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = './databases/currency.db'
        self.csv_path = './csv/cards.csv'
        self.owned_cards_path = './csv/owned_cards.csv'
        self.db = self.create_or_load_database(self.db_path)
        self.create_tables()
        self.cards_data = self.create_or_load_csv(self.csv_path)
        self.owned_cards_data = self.create_or_load_owned_cards(self.owned_cards_path)
        self.active_auction = None
        self.default_channel_name = "general"
        self.last_generated_card = None
        self.claim_pots = {}
        self.current_pot = 0

    def create_or_load_database(self, db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db_exists = os.path.exists(db_path)
        db = sqlite3.connect(db_path)
        if not db_exists:
            print(f"Database {db_path} not found. Creating new database...")
        return db

    def create_tables(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            gold INTEGER DEFAULT 0
        )''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS cards (
            card_id INTEGER PRIMARY KEY,
            name TEXT,
            level TEXT,
            rarity TEXT,
            value INTEGER,
            quantity INTEGER
        )''')
        self.db.commit()

    def create_or_load_csv(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'level', 'rarity', 'value', 'id', 'quantity'])
                writer.writerow(['Luffy', 'Gear 1', 'Rare', '1000', '123456', '1'])
                writer.writerow(['Goku', 'SS1', 'Ultra Rare', '5000', '234567', '3'])
                writer.writerow(['Naruto', 'Sage Mode', 'Legendary', '10000', '345678', '2'])
                writer.writerow(['Ichigo', 'Bankai', 'Epic', '8000', '456789', '5'])

        cards = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cards.append({
                    "name": row['name'],
                    "level": row['level'],
                    "rarity": row['rarity'],
                    "value": int(row['value']),
                    "id": int(row['id']),
                    "quantity": int(row['quantity'])
                })
        return cards

    def create_or_load_owned_cards(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'level', 'rarity', 'value', 'id', 'quantity', 'ownedby'])

        owned_cards = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                owned_cards.append({
                    "name": row['name'],
                    "level": row['level'],
                    "rarity": row['rarity'],
                    "value": int(row['value']),
                    "id": int(row['id']),
                    "quantity": int(row['quantity']),
                    "ownedby": int(row['ownedby'])
                })
        return owned_cards

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")
        self.card_interval.start()
        self.gold_event.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        gold_awarded = random.randint(1, 50)
        self.update_gold(message.author.id, gold_awarded)

    def get_gold(self, user_id):
        cur = self.db.execute("SELECT gold FROM users WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        return result[0] if result else 0

    def update_gold(self, user_id, amount):
        current_gold = self.get_gold(user_id)
        new_gold = max(current_gold + amount, 0)  # Ensure gold doesn't go below 0
        self.db.execute("REPLACE INTO users (user_id, gold) VALUES (?, ?)", (user_id, new_gold))
        self.db.commit()
        return True

    @commands.command()
    async def bank(self, ctx):
        user_id = ctx.author.id
        gold_amount = self.get_gold(user_id)
        await ctx.send(f"{ctx.author.mention}, you have a total of {gold_amount} gold.")

    @commands.command()
    async def pay(self, ctx, member: discord.Member, amount: int):
        if ctx.channel.name != self.default_channel_name:
            await ctx.send(f"This command can only be used in the '{self.default_channel_name}' channel.")
            return
        payer_id = ctx.author.id
        receiver_id = member.id
        if payer_id == receiver_id:
            await ctx.send("You can't send gold to yourself!")
            return
        payer_gold = self.get_gold(payer_id)
        if payer_gold < amount:
            await ctx.send("You don't have enough gold!")
            return
        self.update_gold(payer_id, -amount)
        self.update_gold(receiver_id, amount)
        await ctx.send(f"{ctx.author.name} paid {amount} gold to {member.name}")

    @tasks.loop(hours=1)
    async def card_interval(self):
        card = random.choice(self.cards_data)
        if card["quantity"] > 0:
            self.last_generated_card = card
            card_embed = self.create_card_embed(card)
            general_channel = discord.utils.get(self.bot.get_all_channels(), name=self.default_channel_name)
            if general_channel:
                await general_channel.send(f"🎉 A new card is available for sale! To buy it, use the command `..buy`. 🎉")
                await general_channel.send(embed=card_embed)

    def create_card_embed(self, card):
        embed = discord.Embed(
            title=f"{card['name']} (Level: {card['level']})",
            description=f"Rarity: {card['rarity']}\nValue: {card['value']} gold\nCard ID: {card['id']}\n{card['quantity']} of this card are available."
        )
        return embed

    @commands.command()
    async def buy(self, ctx):
        if ctx.channel.name != self.default_channel_name:
            await ctx.send(f"This command can only be used in the '{self.default_channel_name}' channel.")
            return
        user_id = ctx.author.id
        if self.last_generated_card is None:
            await ctx.send("No card has been generated recently!")
            return
        card = self.last_generated_card
        user_gold = self.get_gold(user_id)
        if user_gold < card["value"]:
            await ctx.send("You don't have enough gold!")
            return
        self.update_gold(user_id, -card["value"])
        self.update_card_quantity(card["id"], -1)
        self.add_card_to_user_collection(card, user_id)
        await ctx.send(f"You have bought {card['name']} for {card['value']} gold!")

    def add_card_to_user_collection(self, card, user_id):
        owned_cards = self.create_or_load_owned_cards(self.owned_cards_path)
        existing_card = next((item for item in owned_cards if item['id'] == card['id'] and item['ownedby'] == user_id), None)
        if existing_card:
            existing_card['quantity'] += 1
        else:
            new_entry = {
                "name": card['name'],
                "level": card['level'],
                "rarity": card['rarity'],
                "value": card['value'],
                "id": card['id'],
                "quantity": 1,
                "ownedby": user_id
            }
            owned_cards.append(new_entry)
        self.save_owned_cards_to_csv(owned_cards)

    def save_owned_cards_to_csv(self, owned_cards):
        with open(self.owned_cards_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'level', 'rarity', 'value', 'id', 'quantity', 'ownedby'])
            for card in owned_cards:
                writer.writerow([card['name'], card['level'], card['rarity'], card['value'], card['id'], card['quantity'], card['ownedby']])

    def update_card_quantity(self, card_id, quantity_change):
        for card in self.cards_data:
            if card['id'] == card_id:
                card['quantity'] += quantity_change
                break
        self.save_cards_to_csv(self.cards_data)

    def save_cards_to_csv(self, cards):
        with open(self.csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'level', 'rarity', 'value', 'id', 'quantity'])
            for card in cards:
                writer.writerow([card['name'], card['level'], card['rarity'], card['value'], card['id'], card['quantity']])

    @commands.command()
    async def collection(self, ctx):
        user_id = ctx.author.id
        owned_cards = self.create_or_load_owned_cards(self.owned_cards_path)
        view = View(timeout=180)
        user_cards = [card for card in owned_cards if card['ownedby'] == user_id]
        if not user_cards:
            await ctx.author.send("You don't own any cards.")
            return
        for card in user_cards:
            button = Button(label=card["name"], custom_id=str(card["id"]))
            view.add_item(button)
            async def button_callback(interaction, card=card):
                if interaction.user.id == user_id:
                    await self.show_card_details(interaction, card)
                else:
                    await interaction.response.send_message("This is not your card!", ephemeral=True)
            button.callback = button_callback
        await ctx.author.send("Here are your owned cards:", view=view)

    async def show_card_details(self, interaction, card):
        embed = discord.Embed(
            title=f"{card['name']} (Level: {card['level']})",
            description=f"Rarity: {card['rarity']}\nValue: {card['value']} gold\nCard ID: {card['id']}\nQuantity: {card['quantity']}"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.loop(minutes=15)
    async def gold_event(self):
        for guild in self.bot.guilds:
            general_channel = discord.utils.get(guild.text_channels, name=self.default_channel_name)
            print("Gold_event attempted")
            if general_channel is not None and random.random() < 0.05:
                print("Gold_event active")
                themed_lines = [
                    "Uh-oh. Buu make bad and break bank. Here! Buu give money! Who take?",
                    "Buu feel generous! Who want Buu's gold? Raise hand!",
                    "Buu hungry for fun! Gold for everyone! Who join?",
                    "Buu say, 'Surprise! Gold falling from sky! Who catch it?'",
                    "Buu have lots of gold! Who want to play with Buu's gold?"
                ]
                themed_message = random.choice(themed_lines)
                self.current_pot = random.randint(500, 20000)
                await general_channel.send(f"{themed_message}\n\n💰A gold raffle has occurred! You can participate to win {self.current_pot} gold! Type `..join` to enter.💰")
                await asyncio.sleep(30)
                await self.process_raffle(general_channel)

    async def process_raffle(self, general_channel):
        if not self.claim_pots:
            await general_channel.send("No one participated in the raffle this time!")
            return
        winner_id = random.choice(list(self.claim_pots.keys()))
        winner = general_channel.guild.get_member(winner_id)
        if winner is not None:
            self.update_gold(winner_id, self.current_pot)
            await general_channel.send(f"Congratulations {winner.mention}! 🎉 You have won {self.current_pot} gold!")
        self.claim_pots.clear()

    @commands.command()
    async def join(self, ctx):
        if ctx.channel.name != self.default_channel_name:
            await ctx.send(f"This command can only be used in the '{self.default_channel_name}' channel.")
            return
        member_id = ctx.author.id
        if member_id in self.claim_pots:
            await ctx.send("You've already entered the raffle!")
            return
        self.claim_pots[member_id] = True
        await ctx.author.send(f"You have entered the gold raffle for {self.current_pot} gold!")

    @gold_event.before_loop
    async def before_gold_event(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def balance(self, ctx):
        user_id = ctx.author.id
        user_gold = self.get_gold(user_id)
        await ctx.send(f"{ctx.author.mention}, you have {user_gold} gold.")

async def setup(bot):
    await bot.add_cog(Currency(bot))