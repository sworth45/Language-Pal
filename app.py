from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)

# Sample data
available_languages = ['French', 'English', 'Spanish', 'Czech']
favorite_languages = ['French', 'English']

# Tracks message counts
language_counts = {
    'French': 0,
    'English': 0,
    'Spanish': 0,
    'Czech': 0
}

# Store previous conversations
conversations = {
    'French': [],
    'English': [],
    'Spanish': [],
    'Czech': []
}

@app.route('/')
def home():
    """
    Home function
    """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Hardcoded login function that always redirects to home
    """
    if request.method == 'POST':
        return redirect(url_for('home'))
    
    return render_template('login.html')


@app.route('/languages')
def languages():
    """
    Languages function
    """
    return jsonify({
        'favorites': favorite_languages,
        'languages': [lang for lang in available_languages
                      if lang not in favorite_languages]
    })


@app.route('/<language>/')
def chat(language):
    """
    Render the chat page for the selected language.
    """
    language = language.capitalize()
    
    if language in available_languages:
        return render_template('chat.html', language=language)
    else:
        return redirect(url_for('home'))


@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Receive the user's message and return a predefined response.
    """
    data = request.get_json()
    language = data.get('language')
    user_message = data.get('message')

    response_message = "This is a static response for testing."

    if language == "French":
        if language_counts["French"] == 0:
            language_counts["French"] += 1
            response_message = "Bonjour"
        elif language_counts["French"] == 1:
            language_counts["French"] += 1
            response_message = "Ça va bien. Où es-tu?"
        elif language_counts["French"] == 2:
            response_message = "Au revoir!"
    elif language == "Czech":
        if language_counts["Czech"] == 0:
            language_counts["Czech"] += 1
            response_message = "Ahoj!"
        elif language_counts["Czech"] == 1:
            language_counts["Czech"] += 1
            response_message = "Jaký máš plán na dnešní den?"

    # Store the conversation
    conversations[language].append({'user': user_message, 'bot': response_message})

    return jsonify({'response': response_message, 'conversations': conversations[language]})



@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    data = request.get_json()
    language = data.get('language')
    user_message = data.get('user')
    bot_response = data.get('bot')

    if language not in conversations:
        conversations[language] = []

    conversations[language].append({'user': user_message, 'bot': bot_response})

    return jsonify(success=True)

@app.route('/get_conversation/<language>', methods=['GET'])
def get_conversation(language):
    return jsonify(conversations.get(language, []))

if __name__ == "__main__":
    app.run(debug=True)
