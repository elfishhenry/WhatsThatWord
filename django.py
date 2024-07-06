import os
import hmac
import hashlib
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# ... other imports and code ...

@csrf_exempt 
@require_POST
def discord_interaction_endpoint(request):
    # --- Discord Signature Verification ---
    signature_header = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')

    if not signature_header or not timestamp:
        return HttpResponse(status=400, content="Missing signature headers")

    body = request.body.decode("utf-8")

    # Your Discord public key (as bytes) - replace with your actual key
    PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY').encode() 

    try:
        message = timestamp.encode() + body.encode()
        hmac.new(PUBLIC_KEY, message, hashlib.sha256).hexverify(signature_header)
    except Exception as e:
        print(f"Verification failed: {e}")  # Log the error for debugging
        return HttpResponse(status=401, content="Invalid request signature")

    # --- Process Verified Interactions ---
    interaction_data = json.loads(body)
    interaction_type = interaction_data['type']

    if interaction_type == 1:  # PING
        return HttpResponse(json.dumps({'type': 1}))  # Respond with PONG

    elif interaction_type == 2:  # APPLICATION_COMMAND
        command_data = interaction_data['data']
        command_name = command_data['name']

        # ... Handle slash commands based on command_name ...
        if command_name == "my_command":
            # ... Execute command logic ...
            return HttpResponse(json.dumps({
                'type': 4,  # Channel message with source
                'data': {
                    'content': 'Command response message'
                }
            }))

    # ... Handle other interaction types as needed ...

    return HttpResponse(status=400)  # Bad Request for unhandled types
