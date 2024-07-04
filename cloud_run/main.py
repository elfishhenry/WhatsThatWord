import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import ezcord
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# pylint: disable=C0103
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load the secret key from an environment variable
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
# Get the webhook URL from the environment variable
webhook_url = os.getenv("WEBHOOK_URL")

# If the webhook URL is not set, prompt the user for input
if not webhook_url:
    webhook_url = input("Enter your webhook URL: ")

bot = ezcord.Bot(
    intents=discord.Intents.default(),
    #error_webhook_url = input("Error Webhook url: "),
    error_webhook_url = os.getenv("ERROR_WEBHOOK_URL"),
    language='auto',
    default_language="en",
)

# Define a simple model for storing poll data
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.JSON, nullable=False, default=lambda: {})

    def __repr__(self):
        return f"<Poll {self.question}>"

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

# Example route to create a new poll
@app.route('/create_poll', methods=['POST'])
def create_poll():
    question = request.form.get('question')
    options = request.form.get('options')
    new_poll = Poll(question=question, options=options)
    db.session.add(new_poll)
    db.session.commit()
    return 'Poll created successfully!'

# Example route to get poll results
@app.route('/poll/<poll_id>')
def get_poll_results(poll_id):
    poll = Poll.query.get(poll_id)
    if poll:
        return render_template('poll_results.html', poll=poll)
    else:
        return 'Poll not found', 404

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.run(os.getenv("DISCORD_TOKEN"))  # Replace with your bot token
