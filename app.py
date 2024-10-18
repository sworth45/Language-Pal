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


if __name__ == "__main__":
    app.run(debug=True)
