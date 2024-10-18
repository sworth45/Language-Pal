""" App file for language pal """

from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Sample data
available_languages = ['French', 'English', 'Spanish', 'Czech']
favorite_languages = ['French', 'English']


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
    # Convert the language from URL back to a readable
    #  format (capitalize first letter, etc.)
    language = language.capitalize()

    # Render the chat page
    #  (you can create a separate chat.html template for this)
    return render_template('chat.html', language=language)



if __name__ == "__main__":
    app.run(debug=True)
