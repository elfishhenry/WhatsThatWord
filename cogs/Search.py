import discord
from discord.ext import commands
import requests
import random
import json
import ezcord
import aiohttp

class Search(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.slash_command(name="search_app", description="Search for a Discord bot in the app directory")
    async def search_app(self, ctx):
        # Hypothetical API endpoint for searching Discord's app directory
        api_url = f"https://discord.com/application-directory/"

        await ctx.respond(api_url)

    '''        async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        if response.content_type == 'application/json':
                            data = await response.json()
                            # Process and format the data as needed
                            if data['results']:
                                app_info = data['results'][0]  # Example to get the first result
                                app_details = (
                                    f"**Name**: {app_info['name']}\n"
                                    f"**Description**: {app_info['description']}\n"
                                    f"**URL**: {app_info['url']}"
                                )
                            else:
                                app_details = "No app found with that name."
                        else:
                            app_details = "Unexpected content type received."
                    else:
                        app_details = "Failed to retrieve data from the app directory."

            await ctx.respond(f"Search result for '{app_name}':\n{app_details}")'''

    @commands.slash_command(name="urban", description="Get the definition of a term(word) from Urban Dictionary.")
    async def urban(self, ctx, *, word: str):
        """
        Fetch and display a definition from Urban Dictionary.

        Parameters:
        - ctx: The context in which the command was invoked.
        - word: The term to look up on Urban Dictionary.

        This command fetches a random definition of the given word from Urban Dictionary
        and displays it in an embedded message with a link to the full entry.
        """
        # Make a GET request to the Urban Dictionary API for the given word
        response = requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
        data = response.json()

        # Check if the API returned any definitions
        if not data["list"]:
            await ctx.respond(f"No definitions found for '{word}'.")
            return

        result = data["list"]
        random_choice = result[0] if result else None 

        # Create an embed with the definition and related information
        embed = discord.Embed(title=f"{word.capitalize()}", description=None, color=0x00FFFF)
        embed.add_field(name="Definition", value=f">>> {random_choice['definition']}", inline=False)
        embed.add_field(name="Example", value=f"{random_choice['example']}", inline=False)
        embed.add_field(name=f"🖒 {random_choice['thumbs_up']}", value="", inline=True)
        embed.add_field(name=f"🖓 {random_choice['thumbs_down']}", value="", inline=True)
        embed.set_footer(text=f"Written on: {random_choice['written_on']}")
        embed.set_author(name=f"Author: {random_choice['author']}")

        # Create a button linking to the full entry on Urban Dictionary
        button = discord.ui.Button(
            label="Check Out",
            url=random_choice["permalink"],
            style=discord.ButtonStyle.link
        )

        # Add the button to a view
        view = discord.ui.View()
        view.add_item(button)

        # Send the embed with the button as a view
        await ctx.respond(embed=embed, view=view)

    
    
   

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Search(bot)) # add the cog to the bot