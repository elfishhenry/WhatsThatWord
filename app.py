from flask import Flask, request, jsonify
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import discord
from discord.ext import commands
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import base64
from dotenv import load_dotenv
import google.generativeai as genai
import pathlib
load_dotenv()
from googleapiclient.discovery import build
# Create an instance of the Flask application

app = Flask(__name__)

# Retrieve the Discord public key from your properties file
DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')


GEMINI_PROJECT_ID = os.getenv("GEMINI_PROJECT_ID")

# Access your API key as an environment variable.
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash')


def verify_discord_request(public_key, signature, timestamp, body):
    """Verifies the signature of a Discord interaction request."""
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False

@app.route('/interactions', methods=['POST'])
def interactions():
    # Verify the request signature
    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    body = request.get_data().decode("utf-8")

    if not verify_discord_request(DISCORD_PUBLIC_KEY, signature, timestamp, body):
        return jsonify({'message': 'Invalid request signature'}), 401

    # Parse the interaction data
    interaction_data = request.get_json()
    interaction_type = interaction_data.get("type")
    
    if interaction_type == 2:  # Application Command Interaction
        command_data = interaction_data.get("data")
        command_name = command_data.get("name")

        if command_name == "time":
            current_time = datetime.utcnow().strftime('%H:%M:%S')
            response_data = {
                "type": 4,  # Channel Message with Source
                "data": {
                    "content": f"The current time is {current_time}"
                }
            }
            return jsonify(response_data)



        if command_name == "image_quote":
            # Get the message object from the interaction data
            message_data = interaction_data['data']['resolved']['messages'][
                str(interaction_data['data']['target_id'])
            ]
            # Access message content and author information
            message_content = message_data['content']
            author_name = message_data['author']['username']
            author_discriminator = message_data['author']['discriminator']
            author_id = message_data['author']['id']

            # --- Image Loading and Preparation ---
            try:
                background_path = "/home/henry/PollBot/cogs/simple-background-with-gradient-shape-green-vector.jpg"
                background_image = Image.open(background_path).resize((500, 250))
            except FileNotFoundError:
                return jsonify({'message': 'Background image not found!'}), 500

            # --- Profile Picture ---
            # Use message.author for the quoted user's profile picture
            asset = interaction_data['data']['resolved']['users'][str(author_id)]['avatar']
            profile_pic_url = f"https://cdn.discordapp.com/avatars/{author_id}/{asset}.png"
            
            response = requests.get(profile_pic_url)
            response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)
            
            with Image.open(BytesIO(response.content)) as img:
                profile_pic = img.convert("RGBA")

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
            combined_text = f"{author_name}#{author_discriminator} was quoted by {interaction_data['member']['user']['username']}#{interaction_data['member']['user']['discriminator']}:" 
            left, top, right, bottom = font.getbbox(combined_text) # Get text dimensions
            text_width = right - left
            text_height = bottom - top
            draw.text((70, 15), combined_text, fill="white", font=font)  # White text

            # --- Message Content --- (Dynamically adjust font size)
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
                encoded_image = base64.b64encode(image_binary.getvalue()).decode('utf-8')

            response_data = {
                "type": 4,  # Channel Message with Source
                "data": {
                    "content": f" ",
                    "attachments": [
                        {
                            "id": 0,
                            "description": "Image Quote",
                            "filename": "image_quote.png",
                            "content_type": "image/png",
                            "data": {
                                "base64": encoded_image
                            }
                        }
                    ]
                }
            }
            return jsonify(response_data)

        if command_name == "ai":
            prompt = command_data.get("options")[0].get("value")
            response = model.generate_content(prompt, stream=True)
            full_response = ""  

            for chunk in response:
                full_response += chunk.text

            response_data = {
                "type": 4,  # Channel Message with Source
                "data": {
                    "content": f"Thinking...",
                    "flags": 64, # Make the initial response ephemeral
                }
            }
            return jsonify(response_data)

    return jsonify({'type': 1}) # Respond with a Pong interaction

if __name__ == '__main__':
    app.run(debug=True)
