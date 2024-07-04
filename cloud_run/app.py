from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a simple model for storing poll data
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.JSON, nullable=False, default=lambda: {})

    def __repr__(self):
        return f"<Poll {self.question}>"

@app.route('/')
def index():
    polls = Poll.query.all()
    return render_template('index.html', polls=polls)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        options = request.form['options']
        new_poll = Poll(question=question, options=options)
        db.session.add(new_poll)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    choice = request.form['choice']
    if choice in poll.votes:
        poll.votes[choice] += 1
    else:
        poll.votes[choice] = 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/poll/<int:poll_id>')
def poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    return render_template('poll.html', poll=poll)

if __name__ == '__main__':
    app.run(debug=True)
