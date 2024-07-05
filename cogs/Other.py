import json
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


load_dotenv()

TENOR_API_KEY = os.getenv("TENOR_API_KEY")
webhook_url = os.getenv("WEBHOOK_URL")


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # command to send feedback to the bot developer via a webhook

    @commands.slash_command(
            name="feedback", 
            description="Send feedback to the bot developer",
                integration_types={
                    discord.IntegrationType.guild_install,
                    discord.IntegrationType.user_install,
                  }, 
                )
    async def feedback(self, ctx, *, feedback: str):
        await ctx.respond("Thanks for the feedback! I'll pass it along to the developer.")

        # Create a session specifically for this webhook request
        with requests.Session() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.send(f"Feedback from {ctx.author.name} ({ctx.author.id}): {feedback}")

    # command to get the current time
    @commands.slash_command(
        name="time", 
        description="Get the current time",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def time(self, ctx):
        await ctx.respond(f"The current time is {discord.utils.utcnow().strftime('%H:%M:%S')}")

    # command to get the current date
    @commands.slash_command(
        name="date", 
        description="Get the current date",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def date(self, ctx):
        await ctx.respond(f"The current date is {discord.utils.utcnow().strftime('%Y-%m-%d')}")

    # command to get the current date and time
    @commands.slash_command(
        name="datetime", 
        description="Get the current date and time",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def datetime(self, ctx):
        await ctx.respond(f"The current date and time is {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

    @commands.slash_command(
        name="tenor", 
        description="Search for a GIF on Tenor",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def tenor(self, ctx, *, query: str):
        await ctx.response.defer()  # Defer the response to give us time to get the GIF

        # Construct the Tenor API URL
        api_url = f"https://tenor.googleapis.com/v2/search?q={query}&key={TENOR_API_KEY}&client_key=my_test_app&limit=8"

        try:
            # Make a GET request to the Tenor API
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the JSON response
            data = response.json()

            # Check if any GIFs were found
            if data["results"]:
                # Get the first GIF result
                gif_url = data["results"][0]["media_formats"]["gif"]["url"]
                

                # Create an embed with the GIF
                embed = discord.Embed(title=f"GIF for '{query}'", color=discord.Color.blue())
                embed.set_image(url=gif_url)

                # Send the embed with the GIF
                await ctx.followup.send(embed=embed)
            else:
                await ctx.followup.send(f"No GIFs found for '{query}'.")

        except requests.exceptions.RequestException as e:
            await ctx.followup.send(f"An error occurred while fetching the GIF: {e}")
        except json.decoder.JSONDecodeError as e:
            await ctx.followup.send(f"Invalid response from Tenor API: {e}")



def setup(bot):
    bot.add_cog(Other(bot))
