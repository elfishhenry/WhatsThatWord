import discord
import os
import ezcord
from dotenv import load_dotenv

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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")
    print("Loading cogs...")
    print("------")
    status = discord.Game(f"Searching")
    await bot.change_presence(status=discord.Status.online, activity=status)

bot.load_cogs("cogs")
bot.run(os.getenv("DISCORD_TOKEN"))  # Replace with your bot token