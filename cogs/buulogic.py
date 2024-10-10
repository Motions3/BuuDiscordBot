import discord
import random
import re
import time
from discord.ext import commands
from collections import deque


class BuuLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


        # Buu's vocabulary and phrases
        self.greetings = ["Hi hi!", "Hello you!", "Buu here!", "You talk to Buu?", "Buu say hi!", "Friend!"]

        # Expanded vocabulary and phrases for Buu
        self.greetings.extend([
            "Buu happy to see you!", "Buu say hello!", "You talk to Buu now!", "Friend here again, yay!",
            "Buu like talking to you!", "What you want to ask Buu today?", "Buu wave hand at you!"
        ])

        # Initializing Buu's phrases to avoid the AttributeError
        self.confused_phrases = ["Buu confused!", "What that mean?", "Buu no understand!", "You speak funny!",
                                 "Buu's head hurt!"]
        self.greetings = ["Hi hi!", "Hello you!", "Buu here!", "You talk to Buu?", "Buu say hi!", "Friend!"]
        self.jokes = ["Buu no think Buu is funny, but Buu try!"]

        # Expanded vocabulary and phrases for Buu
        self.greetings.extend([
            "Buu happy to see you!", "Buu say hello!", "You talk to Buu now!", "Friend here again, yay!",
            "Buu like talking to you!", "What you want to ask Buu today?", "Buu wave hand at you!"
        ])

        self.confused_phrases.extend([
            "Buu head hurt!", "Why you talk like that?", "Buu no understand big words!",
            "Buu try, but Buu confused!", "What you mean?", "Buu think you make no sense!",
            "Buu no smart enough for this!"
        ])

        self.jokes = [
            "Why Buu no tell jokes? Buu not good at them!", "Knock knock. Who there? Buu!",
            "Why Buu no cross road? Buu too busy eating chocolate!",
            "Why sky blue? Buu think because it not red!", "What did one Buu say to other? Let’s eat chocolate!",
            "Buu no think Buu is funny, but Buu try!"
        ]

        self.responses = {
            'time': ["Buu say it time for chocolate!", "Buu no care about time, Buu hungry!",
                     "Time? It's time to talk to Buu!"],
            'day': ["It’s a happy day!", "Buu think today is friend day!", "Buu not sure, but it's good day!"],
            'food': ["Buu love food, especially chocolate!", "You have food? Buu hungry!", "Buu like sweets the best!"],
            'weather': ["Buu no care about weather, Buu only care about chocolate!",
                        "Buu say it's sunny because Buu happy!"],
            'e_mc2': ["Buu no know what that is! Is it food?", "Buu think it's something smart... Buu not smart!",
                      "Why you ask Buu that? Buu no scientist!"]
        }

        self.confused_phrases.extend([
            "Buu head hurt!", "Why you talk like that?", "Buu no understand big words!",
            "Buu try, but Buu confused!", "What you mean?", "Buu think you make no sense!",
            "Buu no smart enough for this!"
        ])

        self.jokes = [
            "Why Buu no tell jokes? Buu not good at them!", "Knock knock. Who there? Buu!",
            "Why Buu no cross road? Buu too busy eating chocolate!",
            "Why sky blue? Buu think because it not red!", "What did one Buu say to other? Let’s eat chocolate!",
            "Buu no think Buu is funny, but Buu try!"
        ]

        self.responses = {
            'time': ["Buu say it time for chocolate!", "Buu no care about time, Buu hungry!",
                     "Time? It's time to talk to Buu!"],
            'day': ["It’s a happy day!", "Buu think today is friend day!", "Buu not sure, but it's good day!"],
            'food': ["Buu love food, especially chocolate!", "You have food? Buu hungry!", "Buu like sweets the best!"],
            'weather': ["Buu no care about weather, Buu only care about chocolate!",
                        "Buu say it's sunny because Buu happy!"],
            'e_mc2': ["Buu no know what that is! Is it food?", "Buu think it's something smart... Buu not smart!",
                      "Why you ask Buu that? Buu no scientist!"]
        }

        self.confused_phrases = ["Buu confused!", "What that mean?", "Buu no understand!", "You speak funny!",
                                 "Buu's head hurt thinking!"]
        self.happy_phrases = ["Buu happy!", "Yay!", "Weeee!", "Buu like that!", "Buu feel good!", "Buu want dance!"]
        self.angry_phrases = ["Buu mad!", "You make Buu angry!", "Grrr!", "Buu no like!", "Buu want smash!"]
        self.hungry_phrases = ["Buu hungry!", "Feed Buu now!", "Buu want eat!", "Gimme food!", "Buu's tummy rumble!"]
        self.sleepy_phrases = ["Buu sleepy...", "Buu take nap now.", "Zzz...", "Buu tired.", "Buu's eyes heavy..."]

        # Buu's interests and knowledge
        self.foods = ["candy", "chocolate", "cake", "ice cream", "cookies", "pudding", "lollipop", "gummy bears",
                      "marshmallows", "cupcakes", "donuts", "pie", "cotton candy", "jelly beans", "caramel"]
        self.games = ["tag", "hide and seek", "catch", "wrestling", "rock-paper-scissors", "tickle fight",
                      "make funny faces", "dance contest", "Simon says", "hopscotch", "balloon pop", "musical chairs"]
        self.objects = ["rock", "tree", "mountain", "building", "car", "airplane", "ship", "robot", "giant ball",
                        "big hammer", "telescope", "trampoline", "bicycle", "kite", "bubble machine"]
        self.topics = ["adventure", "magic", "fighting", "food", "transforming", "flying", "making friends",
                       "being strong", "having fun", "exploring", "learning new things", "helping others",
                       "telling jokes", "solving puzzles"]
        self.dislikes = ["vegetables", "homework", "waiting", "being quiet", "complicated things", "mean people",
                         "cleaning", "medicine", "brushing teeth", "following rules", "sitting still", "being alone"]
        self.emotions = ["happy", "sad", "angry", "excited", "confused", "surprised", "scared", "sleepy", "proud",
                         "shy", "curious", "silly"]

        # Buu's abilities and traits
        self.abilities = ["transform", "regenerate", "absorb", "stretch", "fly", "shoot beams", "teleport",
                          "make candy", "copy moves", "grow stronger"]
        self.traits = ["childish", "powerful", "unpredictable", "playful", "naive", "glutton", "moody", "curious",
                       "easily distracted"]

        # More complex response templates
        self.response_templates = [
            "Buu think {subject} {verb} {object}! Maybe Buu try later.",
            "Why you ask Buu about {subject}? Buu just want {desire}! You help Buu?",
            "Buu no care about {subject}. Buu care about {preference}! That more fun!",
            "You talk about {subject}? Buu rather {action}! Come do with Buu!",
            "Buu feel {emotion} when hear about {subject}. Make Buu want to {reaction}! You feel same?",
            "Buu think {subject} silly. Why not {alternative} instead? Buu think that better!",
            "{subject} remind Buu of {association}. Buu {emotion} that! You ever try?",
            "Buu wonder if {subject} taste good? Buu want try! You think it taste like {food}?",
            "Buu no understand {subject}. Can you explain like Buu is... well, Buu? Use small words!",
            "Ooh! {subject} sound fun! Can Buu play with it? Buu promise not break... maybe.",
            "Buu think {subject} and {object} should fight! Buu watch and eat {food}!",
            "{subject} make Buu want to {action}. You join Buu? We have fun together!",
            "Buu hear about {subject} before. Buu forget. Tell Buu again! Buu try remember this time.",
            "Buu have idea! Let's use {subject} to make giant {object}! It be amazing!",
            "Buu think {subject} need more candy. Everything better with candy! You agree?",
            "If Buu had {subject}, Buu would {action} all day! What you do if you had {subject}?",
            "{subject} sounds boring. Can we talk about {preference} instead? That more interesting!",
            "Buu want to learn about {subject}. You teach Buu? Buu be good student... for candy!",
            "Buu think {subject} and {object} would be good friends. Like Buu and candy! You have friend like that?",
            "Buu wonder... if Buu eat {subject}, Buu get {attribute}? Buu want try! You stop Buu?",
            "Buu use {ability} on {subject}! What happen you think? Buu excited to see!",
            "Buu feel {emotion} today. {subject} make Buu feel better? Or Buu need {food}?",
            "Buu remember when Buu first learn about {subject}. Buu was {emotion}! You remember first time?",
            "Buu think {subject} and {object} make good team. Like Buu and {food}! What you think?",
            "If {subject} was flavor, what it taste like? Buu think maybe {food}. You have better idea?",
            "Buu want challenge! You think Buu can {action} while eating {food} and thinking about {subject}?",
            "Buu curious... what happen if Buu use {ability} on {subject}? It be fun or dangerous?",
            "Buu have dream about {subject} last night. In dream, it could {action}! Dreams silly, right?",
            "You ever wish you could {action} like Buu? Buu teach you... if you give Buu {food}!",
            "Buu think world need more {subject}. Make everyone {emotion}! You agree with Buu?",
        ]

        # Mood system
        self.mood = "neutral"
        self.mood_triggers = {
            "happy": ["friend", "play", "fun", "candy", "game"],
            "angry": ["vegetable", "boring", "no", "bad", "stop"],
            "confused": ["why", "how", "what", "when", "explain"],
            "excited": ["new", "adventure", "surprise", "amazing", "wow"],
            "sleepy": ["tired", "night", "bed", "rest", "quiet"]
        }

        # Memory system
        self.memory = deque(maxlen=5)  # Remembers last 5 interactions
        self.last_interaction_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    @commands.command(name="buu")
    async def buu(self, ctx, *, message: str):
        """Responds to user messages with a Majin Buu-like personality"""
        response = self.generate_response(message)
        await ctx.send(response)

        # Update memory
        self.memory.append(message.lower())
        self.last_interaction_time = time.time()

    def generate_response(self, message):
        message = message.lower()

        # Update mood based on message content
        self.update_mood(message)

        # Check if it's been a while since the last interaction
        if time.time() - self.last_interaction_time > 300:  # 5 minutes
            return f"Buu back! Buu was {self.get_activity()}. What we talk about?"

        # Check for specific scenarios
        if re.search(r'\b(hi|hello|hey)\b', message):
            return f"{random.choice(self.greetings)} Buu feeling {self.mood} today!"

        if re.search(r'\b(food|eat|hungry)\b', message):
            return f"{random.choice(self.hungry_phrases)} Buu want {random.choice(self.foods)}! You have?"

        if re.search(r'\b(tired|sleepy|nap|rest)\b', message):
            return f"{random.choice(self.sleepy_phrases)} But Buu no want miss fun!"

        if re.search(r'\b(play|game|fun)\b', message):
            return f"Buu love play! Let's play {random.choice(self.games)}! Buu promise play fair... maybe."

        if re.search(r'\b(fight|strong|power)\b', message):
            return f"Buu very strong! Buu can {random.choice(self.abilities)} and smash {random.choice(self.objects)} easily! You impress?"

        if re.search(r'\b(sad|angry|mad)\b', message):
            return f"{random.choice(self.angry_phrases)} But if you give Buu {random.choice(self.foods)}, Buu feel better! You have?"

        if re.search(r'\b(happy|glad|joy)\b', message):
            return f"{random.choice(self.happy_phrases)} Buu feel good like eating {random.choice(self.foods)}! You happy too?"

        if re.search(r'\b(confus|understand|explain)\b', message):
            return f"{random.choice(self.confused_phrases)} Buu brain hurt. Let's talk about {random.choice(self.topics)} instead! That easier for Buu."

        if any(word in message for word in self.memory):
            return f"Buu remember! We talk about this before. Buu think it {random.choice(['fun', 'boring', 'tasty', 'strange', 'exciting'])}. You remember too?"

        # If no specific scenario, use a random template
        template = random.choice(self.response_templates)
        return template.format(
            subject=random.choice(self.topics + self.objects + self.foods),
            verb=random.choice(
                ["is fun", "is boring", "is tasty", "is strange", "makes Buu laugh", "confuses Buu", "excites Buu"]),
            object=random.choice(self.objects + self.foods),
            desire=random.choice(["eat candy", "play games", "make friends", "take nap", "go on adventure"]),
            preference=random.choice(self.topics + self.foods + self.games),
            action=random.choice(
                ["play", "eat", "sleep", "fight", "dance", "fly", "make jokes", "explore", "transform"]),
            emotion=random.choice(self.emotions),
            reaction=random.choice(
                ["laugh", "cry", "jump", "sing", "dance", "eat more", "take nap", "make friends", "go adventure"]),
            alternative=random.choice(
                ["eat candy", "play game", "make friends", "take nap", "fight bad guys", "learn new thing"]),
            association=random.choice(self.foods + self.games + self.objects),
            attribute=random.choice(
                ["super strength", "ability to fly", "magic powers", "big brain", "stretchy arms", "laser eyes"]),
            food=random.choice(self.foods),
            ability=random.choice(self.abilities)
        )

    def update_mood(self, message):
        for mood, triggers in self.mood_triggers.items():
            if any(word in message for word in triggers):
                self.mood = mood
                break

    def get_activity(self):
        activities = [
            f"eating {random.choice(self.foods)}",
            f"playing {random.choice(self.games)}",
            f"thinking about {random.choice(self.topics)}",
            f"practicing {random.choice(self.abilities)}",
            f"avoiding {random.choice(self.dislikes)}",
            f"feeling {random.choice(self.emotions)}"
        ]
        return random.choice(activities)


async def setup(bot):
    await bot.add_cog(BuuLogic(bot))