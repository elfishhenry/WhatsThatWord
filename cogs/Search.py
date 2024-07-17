import discord
from discord.ext import commands, bridge
import requests
from googlesearch import search
from pytube import YouTube
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


load_dotenv()

ytdatav3 = os.getenv("GCP_API_KEY")

class Search(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @bridge.bridge_command(
        name="youtube", 
        description="Search YouTube videos, returns a selected amount of results",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def youtube(self, ctx, *, query: str, limit: int):
        if limit > 10:
            limit = 10
            await ctx.send("The limit for the (the number you put in the box for limit) amount of results is 10, you're results have automatically been set to 10.")        
        api_key = ytdatav3
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=limit  # Adjust maxResults to fetch up to 10 results
        )
        response = request.execute()
        
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                thumbnail_url = item['snippet']['thumbnails']['default']['url']
                
                embed = discord.Embed(title="YouTube Video", url=video_url, color=discord.Color.blue())
                embed.set_image(url=thumbnail_url)  # Set thumbnail as embed image
                embed.set_footer(text="Click the title to watch on YouTube")
                
                await ctx.respond(content=video_url, embed=embed)


    @bridge.bridge_command(
        name="urban", 
        description="Get the definition of a term(word) from Urban Dictionary.",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
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

    @bridge.bridge_command(
        name="google", 
        description="Google things!",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def google_search(self, ctx: discord.ApplicationContext, query: str):
        await ctx.response.defer()  # Defer the response to give us time to get the search results
        results = list(search(query, num_results=10, safe='on', timeout=15))
        #print(results)

        unique_results = []
        seen_urls = set()
        for result in results:
            if result not in seen_urls:
                seen_urls.add(result)
                unique_results.append(result)

        embed = discord.Embed(title=f"Search results for:", description=f"'{query}'", color=discord.Color.blue())
        
        for i, result in enumerate(unique_results, start=1):
            embed.add_field(name=f"Result {i}", value=result, inline=False)

        await ctx.followup.send(embed=embed)
   
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Search(bot)) # add the cog to the bot
