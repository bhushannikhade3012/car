from flask import Flask, render_template, request
from chatbot_api import apnabot

app = Flask(__name__)
chat_history = []
@app.route('/')
def index():
    return render_template('index.html')  # This is your "Start" page

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Your dashboard page

@app.route('/maintainance', methods=['GET', 'POST'])
def maintenance():
    bot_response = None  # Default response  # Initialize chat history
    global chat_history
    if request.method == 'POST':
        # Capture user message from form
        user_message = request.form.get('user_message', '')
        
        if user_message:
            # Generate bot response using apnabot function
            bot_response, chat_history = apnabot(user_message, chat_history)
    
    # Render maintenance page with the bot response and chat history
    return render_template('maintainance.html', response=bot_response, chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
