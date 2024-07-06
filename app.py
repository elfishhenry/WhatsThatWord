from flask import Flask, request, jsonify
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import discord
from discord.ext import commands
import json
from datetime import datetime

app = Flask(__name__)

# Retrieve the Discord public key from your properties file
DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')

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

    return jsonify({'type': 1}) # Respond with a Pong interaction

if __name__ == '__main__':
    app.run(debug=True)
