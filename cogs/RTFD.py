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
        # Define the options for the select menu
        options = [
            discord.SelectOption(label="py-cord", value="https://docs.pycord.dev/en/stable/", description="Documentation for the py-cord library."),
            discord.SelectOption(label="discord.py", value="https://discordpy.readthedocs.io/en/stable/", description="Documentation for the discord.py library."),
            discord.SelectOption(label="Python 3", value="https://docs.python.org/3/", description="Documentation for Python 3."),
            discord.SelectOption(label="discord.js", value="https://discord.js.org/", description="Documentation for the discord.js library."),
            discord.SelectOption(label="Discord", value="https://discord.com/developers/docs/intro", description="Official Discord API documentation."),
        ]

        # Create the select menu
        select = discord.ui.Select(
            placeholder="Choose a documentation:",
            options=options
        )

        # Define a callback function for when an option is selected
        async def select_callback(interaction: discord.Interaction):
            # Get the selected option's value (which is the URL)
            selected_url = interaction.data["values"][0]

            # Send the URL to the user who invoked the command
            await interaction.response.send_message(f"Here's the documentation you selected: {selected_url}", ephemeral=True)

        # Set the callback function for the select menu
        select.callback = select_callback

        # Create a view to hold the select menu
        view = discord.ui.View()
        view.add_item(select)

        # Get the bot's application info (which includes the owner)
        app_info = await self.bot.application_info()
        owner = app_info.owner  # Get the owner object
        owner_name = "<@844984362008838244>"

        # Send the message with the select menu, pinging the user
        await ctx.respond(f"||{message.author.mention},|| **Choose a documentation:** Want a new documentation added? Tell **{owner_name}**!", view=view)
    
    @rtfd.error
    async def secret_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("You can't use this command!")
        else:
            raise error 

def setup(bot):
    bot.add_cog(RTFD(bot))
