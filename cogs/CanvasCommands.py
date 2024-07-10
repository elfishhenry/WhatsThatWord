from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import discord
from discord.ext import commands
import os # Import the os module

class CanvasCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.message_command(
        name="image_quote",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    async def profile_card(self, ctx, message: discord.Message):
        # Defer the response to allow for processing time
        await ctx.defer()

        # --- Load Background Image ---
        try:
            background_image = Image.open("/home/henry/PollBot/cogs/simple-background-with-gradient-shape-green-vector.jpg")  # Replace with your background image path
        except FileNotFoundError:
            await ctx.respond("Background image not found!")
            return

        # Resize background to desired dimensions if needed
        background_image = background_image.resize((500, 250))  

        # --- Profile Picture ---
        # Use message.author for the quoted user's profile picture
        asset = message.author.display_avatar.with_size(128) 
        await asset.save(f"{message.author.id}.png")
        profile_pic = Image.open(f"{message.author.id}.png").convert("RGBA")

        # Resize the profile picture to fit in a circle
        mask = Image.new("L", profile_pic.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0) + profile_pic.size, fill=255)
        profile_pic.putalpha(mask)
        profile_pic = profile_pic.resize((50, 50)) 

        # Paste the profile picture onto the background image
        background_image.paste(profile_pic, (10, 10), profile_pic)

        # --- Text Drawing ---
        draw = ImageDraw.Draw(background_image)  # Draw on the background image

        # --- Combined "Quoted" and Display Name --- 
        font = ImageFont.truetype("/home/henry/PollBot/cogs/arial.ttf", 22) 
        # Use message.author for the quoted user's display name
        combined_text = f"{message.author.display_name} was quoted by {ctx.author.display_name}:" 
        left, top, right, bottom = font.getbbox(combined_text) # Get text dimensions
        text_width = right - left
        text_height = bottom - top
        draw.text((70, 15), combined_text, fill="white", font=font)  # White text

        # --- Message Content --- (Dynamically adjust font size)
        message_content = message.content  
        initial_font_size = 48
        font = ImageFont.truetype("/home/henry/PollBot/cogs/arial.ttf", initial_font_size)
        min_font_size = 12  # Set your desired minimum font size

        # Adjust font size until text fits within width or minimum size is reached
        while True:
            left, top, right, bottom = draw.multiline_textbbox((0, 0), message_content, font=font)
            text_width = right - left
            if text_width <= background_image.width * 0.95 or initial_font_size <= min_font_size:
                break
            initial_font_size -= 2
            font = ImageFont.truetype("/home/henry/PollBot/cogs/arial.ttf", initial_font_size)

        # Calculate x-coordinate to ensure text stays within the right margin
        x_coordinate = min((background_image.width - text_width) / 2.5 + 20, background_image.width - text_width - 20)  

        # Draw the multiline text
        draw.multiline_text((x_coordinate, (background_image.height - text_height) / 2.2), 
                            message_content, fill="white", font=font)

        # Save the image to a BytesIO object
        with BytesIO() as image_binary:
            background_image.save(image_binary, 'PNG')  # Save the background image
            image_binary.seek(0)

            # Send the image as a file
            await ctx.respond(file=discord.File(fp=image_binary, filename='profile_card.png'))

        # Delete the profile picture file after sending the quote
        os.remove(f"{message.author.id}.png") 

def setup(bot):
    bot.add_cog(CanvasCommands(bot))
