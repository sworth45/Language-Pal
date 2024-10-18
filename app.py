""" App file for language pal """

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Sample data
available_languages = ['French', 'English', 'Spanish', 'Czech']
favorite_languages = ['French', 'English']

# tracks message no
language_counts = {
    'French': 0,
    'English': 0,
    'Spanish': 0,
    'Czech': 0
}


@app.route('/')
def home():
    """
    home function
    """
    return render_template('index.html')


@app.route('/languages')
def languages():
    """
    languages function
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
    # user_message = data.get('message')
    language = data.get('language')
    print(language)

    response_message = "This is a static response for testing."

    if language == "French":
        if language_counts["French"] == 0:
            language_counts["French"] += 1
            response_message = "Bonjour"
        if language_counts["French"] == 1:
            language_counts["French"] += 1
            response_message = "Ca va bein. Ou est-tu?"
        if language_counts["French"] == 2:
            response_message = "Au Revoir!"
    elif language == "Czech":
        if language_counts["Czech"] == 0:
            language_counts["Czech"] += 1
            response_message = "Ahoj!"
        if language_counts["Czech"] == 1:
            language_counts["Czech"] += 1
            response_message = "Jaký máš plán na dnešní den?"

    return jsonify({'response': response_message})


if __name__ == "__main__":
    app.run(debug=True)