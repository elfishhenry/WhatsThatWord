import discord 
from discord.ext import commands
from google_books_api_wrapper.api import GoogleBooksAPI
from dotenv import load_dotenv
import os
from discord.commands.context import ApplicationContext
from discord.commands import option
from google_books_api_wrapper.exceptions import GoogleBooksAPIException
load_dotenv()



def get_book_info_by_title(title):
    try:
        api = GoogleBooksAPI()
        book = api.get_book_by_title(title)
        if book:
            # Ensure Authors is always a list
            authors = [book.authors] if isinstance(book.authors, str) else book.authors
            return {
                "Title": book.title,
                "Authors": authors,
                "Publisher": book.publisher,
                "Published Date": book.published_date,
                "Description": book.description,
                "ISBN-10": book.ISBN_10,
                "ISBN-13": book.ISBN_13,
                "Page Count": book.page_count,
                "Small Thumbnail": book.small_thumbnail,
                "Large Thumbnail": book.large_thumbnail
            }
        else:
            return "No book found with the given title."
    except GoogleBooksAPIException as e:
        return f"An error occurred: {e}"

books = GoogleBooksAPI()

#defines the cog
class bookcog(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @commands.slash_command(
        name="searchbook",
        description="Search for a book.",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    @option(
        "title",
        description="Enter the title of the book: ",
        required=True,
    )
    async def searchbook(self, ctx: ApplicationContext, title):
        await ctx.response.defer()
        info = get_book_info_by_title(title)

        if isinstance(info, str):  # Check if info is a string (error message)
            await ctx.respond(info)
            return

        if isinstance(info, dict):   # Check if info is a dictionary
            embed = discord.Embed(title=info["Title"], description=info["Description"])  # Set title and short description (truncate description)
            embed.set_author(name="Book Information", icon_url="https://cdn.discordapp.com/attachments/your_bot_id/icon.png")  # Set author (replace with your bot's icon URL)
            # Add additional fields
            embed.add_field(name="Authors", value=info["Authors"])
            embed.add_field(name="Publisher", value=info["Publisher"])
            embed.add_field(name="Published Date", value=info["Published Date"])
            embed.add_field(name="Page Count", value=str(info["Page Count"]) + " pages")

            # Add thumbnail if allowed by rate limits (replace with actual URL if available)
            if info.get("Small Thumbnail"):
                embed.set_thumbnail(url=info["Small Thumbnail"])


            await ctx.respond(embed=embed)

# adds the cog
def setup(bot): 
    bot.add_cog(bookcog(bot))