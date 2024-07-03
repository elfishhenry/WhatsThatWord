import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()
import logging
import ezcord


bot = ezcord.Bot(
    intents=discord.Intents.default(),
    error_webhook_url = input(str("Webhook Url: ")),  # Replace with your webhook URL
    default_language="en"
)

log_dir = r"/home/henry/PollBot"


# Bot class with the search command
class MyBot(discord.Bot):
    async def on_ready(self):
        # Register the slash command (replace "search" with your desired command name)
        await self.application_command.sync()  
        print(f"Logged in as {self.user}")



if __name__ == "__main__":
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.run(os.getenv("DISCORD_TOKEN"))