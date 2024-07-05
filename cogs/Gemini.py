from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import google.generativeai as genai
import pathlib


load_dotenv()

GEMINI_PROJECT_ID = os.getenv("GEMINI_PROJECT_ID")


# Access your API key as an environment variable.
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash')



class Gemini(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="ai", description="Ask ai something")
    async def ai(self, ctx, prompt: str):
        await ctx.response.defer()
        response = model.generate_content(prompt, stream=True)
        full_response = ""  # Create an empty string to store the response chunks

        for chunk in response:
            full_response += chunk.text

        embed = discord.Embed(
            title=f"Ai's response to {prompt}.",
            description=full_response,
            color=discord.Colour.dark_purple(),
        )
                
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThr7qrIazsvZwJuw-uZCtLzIjaAyVW_ZrlEQ&s")

        embed.set_footer(text="Like this Ai? Use it in your web-browser by clicking the button below!")
        button = discord.ui.Button(
            label="Gemini AI",
            url="https://gemini.google.com/app",
            style=discord.ButtonStyle.link
        )

        # Add the button to a view
        view = discord.ui.View()
        view.add_item(button)

        await ctx.respond(embed=embed, view=view)
            


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Gemini(bot)) # add the cog to the bot
