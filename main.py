import discord
import os
import ezcord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

webhook_url = os.getenv("ERROR_WEBHOOK_URL")


if not webhook_url:
    webhook_url = input("Enter your webhook URL: ")


# Get the admin server IDs from the environment variable
admin_server_ids = [int(id) for id in os.getenv("ADMIN_SERVER_IDS", "").split(",")]

bot = ezcord.Bot(  
    intents=discord.Intents.default(),
    error_webhook_url=webhook_url,
    language='auto',
    default_language="en",
)
# Add the blacklist functionality
bot.add_blacklist(admin_server_ids)


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
bot.run(os.getenv("testing_token"))
