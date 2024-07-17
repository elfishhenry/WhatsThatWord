import discord
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
            name="support_server",
            description="Provides a link to the support server, in which you can get updates about the bot."
            )
    async def support_server(self, ctx):
        await ctx.respond("Join the support server here: https://discord.gg/Y5rTCzfKR4") # Replace with your actual support server invite link


    @commands.slash_command(
            name="invite", 
            description="Invite the bot to your server",
            integration_types={
                discord.IntegrationType.guild_install,
                discord.IntegrationType.user_install,
            }, 
        )
    async def invite(self, ctx):
        await ctx.respond(f"Invite me to your server [here!](https://discord.com/oauth2/authorize?client_id=1258057927734853684)") # Replace with your actual bot ID

    @commands.slash_command(
        name="info", 
        description="Get information about the bot",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def info(self, ctx):
        embed = discord.Embed(title="Bot Information", color=discord.Color.blue())
        embed.add_field(name="Name", value=self.bot.user.name, inline=False)
        embed.add_field(name="ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="Library", value="Py-cord v2.6.0, EzCord 0.6.5", inline=False)
        embed.add_field(name="Developer", value="<@844984362008838244>", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))