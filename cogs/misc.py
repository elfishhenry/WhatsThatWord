import discord
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot =  bot

    @commands.slash_command(name="help", description="Lists all the commands and their descriptions.")
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

def setup(bot):
    bot.add_cog(misc(bot))