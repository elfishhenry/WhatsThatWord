import discord
import os
import ezcord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

webhook_url = os.getenv("WEBHOOK_URL")

# If the webhook URL is not set, prompt the user for input
if not webhook_url:
    webhook_url = input("Enter your webhook URL: ")
    
bot = ezcord.Bot(
    intents=discord.Intents.default(),
    #error_webhook_url = input("Error Webhook url: "),
    error_webhook_url = os.getenv("ERROR_WEBHOOK_URL"),
    language='auto',
    default_language="en",
)

@bot.slash_command(name="help", description="Lists all the commands and their descriptions.")
async def help(ctx):
    await ctx.response.defer()

    embed = discord.Embed(title="Here's a list of all the commands:", colour=discord.Colour.gold())
    embed.add_field(name="/Youtube", value="Search YouTube videos, returns a selected amount of results", inline=True)
    embed.add_field(name="/Urban", value="Get the definition of a term(word) from Urban Dictionary.", inline=True)
    embed.add_field(name="/Google", value="Google things!", inline=True)
    embed.add_field(name="/Ai", value="Ask ai something", inline=True)
    embed.add_field(name="User_command: Server Info", value="Get information about the server the command is used in.", inline=True)
    embed.add_field(name="User_command: Account Creation Date", value="Get the date the account was created.", inline=True)
    embed.add_field(name="Message_command: Get Message ID", value="Get the ID of the message the command is used in.", inline=True)
    embed.add_field(name="/Tenor", value="Search for a GIF on Tenor", inline=True)
    embed.add_field(name="/Image", value="Send an image as an attachment", inline=True)
    embed.add_field(name="/Feedback", value="Send feedback to the bot developer", inline=True)
    embed.add_field(name="/date", value="Get the current date", inline=True)
    embed.add_field(name="/time", value="Get the current time", inline=True)
    embed.add_field(name="/datetime", value="Get the current date and time", inline=True)
    embed.add_field(name="/ai", value="Ask ai something", inline=True)

    await ctx.respond(embed=embed)






@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")
    print("Loading cogs...")
    print("------")
    status = discord.Game(f"Searching")
    await bot.change_presence(status=discord.Status.online, activity=status)
    print("Status changed!")
    print("------")
    print("Ready!")


bot.load_cogs("cogs")
bot.run(os.getenv("DISCORD_TOKEN"))  # Replace with your bot token