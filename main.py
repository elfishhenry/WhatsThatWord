import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()
import logging

intents = discord.Intents.default()


bot = discord.Bot()

log_dir = r"/home/henry/PollBot"



log_file = os.path.join(log_dir, 'bot.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    logging.info(f"Ping or Latency is {round(bot.latency * 1000)}ms")
    logging.info(f"Pending commands{bot._pending_application_commands}")
    logging.info(f"Slash or application commands{bot._application_commands}")
    logging.info(f"Prefixed commands {bot.commands}")
    print(f'{bot.user} has connected to Discord!')



cogs_list = [
    'Search'
]


for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
    print(f'loaded the cog of the century: {cog}')



bot.run(os.getenv("DISCORD_TOKEN"))