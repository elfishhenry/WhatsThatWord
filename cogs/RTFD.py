import discord
from discord.ext import commands

owner_id = "844984362008838244"

class RTFD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.message_command(
        name="rtfd", 
        description="Search the Python documentation",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    @commands.is_owner()
    async def rtfd(self, ctx, message: discord.Message):
        # Define the buttons and their corresponding URLs
        buttons = [
            discord.ui.Button(label="Pycord", url="https://docs.pycord.dev/en/stable/", style=discord.ButtonStyle.link),
            discord.ui.Button(label="discord.py", url="https://discordpy.readthedocs.io/en/stable/", style=discord.ButtonStyle.link),
            discord.ui.Button(label="Python 3", url="https://docs.python.org/3/", style=discord.ButtonStyle.link),
            discord.ui.Button(label="discord.js", url="https://discord.js.org/", style=discord.ButtonStyle.link),
            discord.ui.Button(label="Discord", url="https://discord.com/developers/docs/intro", style=discord.ButtonStyle.link),
        ]

        # Create a view to hold the buttons
        view = discord.ui.View()
        for button in buttons:
            view.add_item(button)

        # Get the bot's application info (which includes the owner)
        app_info = await self.bot.application_info()
        owner = app_info.owner  # Get the owner object
        owner_name = "<@844984362008838244>"


        # Send the message with the buttons, pinging the user
        await ctx.respond(f"**{message.author.mention}, **Choose a documentation:** **Want a new documentation added? Tell **{owner_name}**!", view=view)

    @rtfd.error
    async def secret_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("You can't use this command!")
        else:
            raise error 

def setup(bot):
    bot.add_cog(RTFD(bot))
