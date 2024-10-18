from flask import Flask, request, render_template, jsonify, redirect, url_for

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
    Login function
    """
    if request.method == 'POST':
        # Process login form (currently hardcoded login)
        username = request.form.get('username')
        password = request.form.get('password')
        
        # You can add real authentication here
        if username == 'admin' and password == 'password':  # Hardcoded example credentials
            return redirect(url_for('home'))  # Redirect to home if login is successful
        else:
            error = "Invalid username or password. Please try again."
            return render_template('login.html', error=error)

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
    return render_template('chat.html', language=language)


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
