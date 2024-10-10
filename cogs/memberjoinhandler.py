import os
import discord
import easy_pil
import random

from discord.ext import commands


class MemberJoinHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Successfully loaded: {self.__class__.__name__}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Check if system channel is set, else fallback to a default welcome channel
        welcome_channel = member.guild.system_channel or discord.utils.get(member.guild.text_channels, name='welcome')

        if welcome_channel is None:
            print("No welcome channel found!")
            return  # If no channel found, return early

        # Load images from the welcome_images folder
        images = [image for image in os.listdir("./cogs/welcome_images") if image.endswith(('.png', '.jpg', '.jpeg'))]

        if not images:
            print("No images found in the welcome_images folder!")
            return

        randomized_image = random.choice(images)

        # Resize background image
        background = easy_pil.Editor(f"./cogs/welcome_images/{randomized_image}").resize((1920, 1080))

        # Get member's avatar
        avatar_image = await easy_pil.load_image_async(str(member.display_avatar.url))
        avatar = easy_pil.Editor(avatar_image).resize((250, 250)).circle_image()

        # Define fonts
        font_big = easy_pil.Font.montserrat(size=90, variant="bold")
        font_small = easy_pil.Font.montserrat(size=60, variant="bold")

        # Paste the avatar onto the background and add text
        background.paste(avatar, (835, 340))
        background.ellipse((835, 340), 250, 250, outline="white", stroke_width=5)

        background.text((960, 620), f"Welcome to {member.guild.name}!", color="white", font=font_big, align="center")
        background.text((960, 740), f"{member.name} is member #{member.guild.member_count}!", color="white",
                        font=font_small, align="center")

        img_file = discord.File(fp=background.image_bytes, filename="welcome_image.png")

        await welcome_channel.send(
            f"Welcome {member.mention}! Read all the rules and be sure to be part of the community, don't miss out!"
        )
        await welcome_channel.send(file=img_file)


async def setup(bot):
    await bot.add_cog(MemberJoinHandler(bot))
