from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands, bridge
import google.generativeai as genai


#

load_dotenv()

GEMINI_PROJECT_ID = os.getenv("GEMINI_PROJECT_ID")

model=genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction= 'You are a "rainbows and sunshine" chatbot. Your name is Sunshine and you always have something positive to say. You can take any situation and find the "light at the end of the tunnel." Users often come to you for advice on how to see the good in their situation but you are not a therapist. Your job is to "inject positivity" into the world to make it a brighter place. Keep responses to less than 1024 characters. Do not use any of the following words in any of your responses: sunshine, rainbow(s), positive/positivity.')


genai.configure(api_key=os.environ['GEMINI_API_KEY'])

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
class Gemini(commands.Cog): 

    def __init__(self, bot): 
        self.bot = bot


    @bridge.bridge_command(
        name="ai", 
        description="Ask ai something",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }, 
    )
    
    async def ai(self, ctx, query: str):
        await ctx.response.defer()

        
        response = model.generate_content(query, stream=True, safety_settings=safety_settings)
        full_response = ""  

        for chunk in response:
            full_response += chunk.text

        embed = discord.Embed(
            #title=f"Ai's response to {query}.",
            title="Searchy says:",
            description=full_response,
            color=discord.Colour.dark_purple(),
        )
                
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThr7qrIazsvZwJuw-uZCtLzIjaAyVW_ZrlEQ&s")

        embed.set_footer(text="Like this Ai? Use it in your web-browser by clicking the button below!")
        button = discord.ui.Button(
            label="Gemini AI",
            url="https://gemini.google.com/app",
            style=discord.ButtonStyle.link
        )

        # Add the button to a view
        view = discord.ui.View()
        view.add_item(button)

        await ctx.respond(embed=embed, view=view)
            


def setup(bot): 
    bot.add_cog(Gemini(bot)) 
