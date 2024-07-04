from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import google.generativeai as genai
import pathlib
import io
from PIL import Image

load_dotenv()

GEMINI_PROJECT_ID = os.getenv("GEMINI_PROJECT_ID")


# Access your API key as an environment variable.
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-pro-image')



class GeminiImage(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="ai_image", description="Ask ai to generate an image")
    async def ai_image(self, ctx, prompt: str):
        await ctx.response.defer()
        response = model.generate_image(prompt)
        image_bytes = response.image_bytes

        # Convert the image bytes to a PIL Image object
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image to a temporary file
        temp_file = io.BytesIO()
        image.save(temp_file, format="PNG")
        temp_file.seek(0)

        # Send the image as a file
        await ctx.respond(file=discord.File(temp_file, "generated_image.png"))
            


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(GeminiImage(bot)) # add the cog to the bot