import json
import discord
from discord.ext import commands, bridge
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import aiohttp
from discord import Webhook
from io import BytesIO



load_dotenv()

TENOR_API_KEY = os.getenv("TENOR_API_KEY")
webhook_url = os.getenv("WEBHOOK_URL")


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.user_command(
        name="Server Info",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },                           
    )
    async def server_info(self, ctx, member: discord.Member):
        # Check if the command is used in a server
        if ctx.guild is None:
            await ctx.respond("This command can only be used in a server.")
            return

        # Get the guild from the context
        guild = ctx.guild

        # Create the embed
        embed = discord.Embed(title=f"{guild.name}'s Server Information", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Server ID:", value=guild.id, inline=False)
        # Removed embed.add_field(name="Owner:", value=guild.owner.mention, inline=False)
        embed.add_field(name="Created At:", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Member Count:", value=guild.member_count, inline=False)
        embed.add_field(name="Text Channels:", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels:", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Roles:", value=len(guild.roles), inline=True)

        await ctx.respond(embed=embed)

    @commands.user_command(
        name="Account Creation Date",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },                           
    ) 
    async def account_creation_date(self, ctx, member: discord.Member):
        await ctx.respond(f"{member.name}'s account was created on {member.created_at}")


    @commands.message_command(
        name="Get Message ID",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def get_message_id(self, ctx, message: discord.Message):
        await ctx.respond(f"Message ID: `{message.id}`")


    @bridge.bridge_command(
            name="feedback", 
            description="Send feedback to the bot developer, I might even respond personally.",
                integration_types={
                    discord.IntegrationType.guild_install,
                    discord.IntegrationType.user_install,
                  }, 
                )
    async def feedback(self, ctx, *, feedback: str):

        embed = discord.Embed(title="Feedback!", description="Thanks for the feedback! I'll pass it along to the developer.", color=discord.Color.blue())
        embed.add_field(name="WARNING!", value="False use of this command will get you blacklisted from using this command in future.", inline=False)

        await ctx.respond(embed=embed)
        async with aiohttp.ClientSession() as session:
            
        # No need to create a separate session here
            webhook = Webhook.from_url(webhook_url, session=session)
            feedback_embed = discord.Embed(title="Feedback", description=feedback, color=discord.Color.blue())
            feedback_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            feedback_embed.set_footer(text=f"ID: {ctx.author.id}")
            
            await webhook.send(embed=feedback_embed)

    # command to get the current time
    @bridge.bridge_command(
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
    @bridge.bridge_command(
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
    @bridge.bridge_command(
        name="datetime", 
        description="Get the current date and time",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def datetime(self, ctx):
        await ctx.respond(f"The current date and time is {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

    @bridge.bridge_command(
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

    @bridge.bridge_command(name="vote", description="Information about how you can help this bot grow.")
    async def vote(self, ctx):
        
        embed = discord.Embed(title="I am now on top.gg and DiscordBotList!", description="To help me grow you can press one of the buttons below to vote for me!")

        # Create the view first
        view = discord.ui.View()

        # Define the first button
        button = discord.ui.Button(
            label="Top.gg",
            url="https://top.gg/bot/1258057927734853684",
            style=discord.ButtonStyle.link
        )
        # Add the button to the view
        view.add_item(button)        

        # Define the second button
        button = discord.ui.Button(
            label="DiscordBotList",
            url="https://top.gg/bot/1258057927734853684",
            style=discord.ButtonStyle.link
        )
        # Add the button to the view
        view.add_item(button)        

        await ctx.respond(embed=embed, view=view)
        
    @bridge.bridge_command(
        name="image",
        description="Send an image as an attachment",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def image(self, ctx, attachment: discord.Attachment):
        """Sends the provided attachment.

        Args:
            attachment (discord.Attachment): The image attachment to send.
        """
        await ctx.response.defer()

        # Check if the attachment is actually an image
        if attachment.content_type and attachment.content_type.startswith('image/'):
            try:
                # Read the image data from the attachment
                image_data = await attachment.read()

                # Create a Discord file object from the image data
                image_file = discord.File(fp=BytesIO(image_data), filename=attachment.filename)

                # Send the image as an attachment
                await ctx.followup.send(file=image_file)

                # Check if the file exists before attempting to delete

            except Exception as e:
                await ctx.followup.send(f"An error occurred while processing the image: {e}")
        else:
            await ctx.followup.send("Please provide a valid image attachment.")



def setup(bot):
    bot.add_cog(Other(bot))
