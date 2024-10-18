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
        # No matter what the input is, redirect to the home page
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


# Move the dynamic route after static routes to avoid conflicts
@app.route('/<language>/')
def chat(language):
    """
    Render the chat page for the selected language.
    """
    # Capitalize language to match
    language = language.capitalize()
    
    if language in available_languages:
        return render_template('chat.html', language=language)
    else:
        # If the language is not available, redirect to home (or handle as you wish)
        return redirect(url_for('home'))


@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Receive the user's message and return a predefined response.
    """
    data = request.get_json()
    language = data.get('language')
    print(language)

    response_message = "This is a static response for testing."

    if language == "French":
        if language_counts["French"] == 0:
            language_counts["French"] += 1
            response_message = "Bonjour"
        elif language_counts["French"] == 1:
            language_counts["French"] += 1
            response_message = "Ca va bien. Où es-tu?"
        elif language_counts["French"] == 2:
            response_message = "Au revoir!"
    elif language == "Czech":
        if language_counts["Czech"] == 0:
            language_counts["Czech"] += 1
            response_message = "Ahoj!"
        elif language_counts["Czech"] == 1:
            language_counts["Czech"] += 1
            response_message = "Jaký máš plán na dnešní den?"

    return jsonify({'response': response_message})


if __name__ == "__main__":
    app.run(debug=True)