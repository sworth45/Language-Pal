from flask import Flask, request, render_template, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, user_data
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key' # TODO: add a secret key

#db = SQLAlchemy(app)

db.init_app(app)


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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    username = session['username']

    return render_template('index.html',username=username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])

def login():
    """
    Hardcoded login function that always redirects to home
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check user existence
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

        # Create a session for the user
        session['user_id'] = user.id
        session['username'] = user.username
        #initializes struct for user
        if(username not in user_data.keys()):
            user_data[user.id] = {}


        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Hardcoded signup function that always redirects to home
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))

        # Hash the password and add user to the database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('signup.html')


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
    time.sleep(1)
    """
    Receive the user's message and return a predefined response.
    """
    data = request.get_json()
    language = data.get('language')
    user_message = data.get('message')

    # FIX
    new_conversation = data.get('new_conversation', False)
    conversation_index = data.get('conversation_index')

    response_message = "This is a static response for testing."
    if language == "Spanish":
        if language_counts["Spanish"] == 0:
            language_counts["Spanish"] += 1
            # Hola
            response_message = "¡Hola! ¿Cómo estas?"
        elif language_counts["Spanish"] == 1:
            language_counts["Spanish"] += 1
            # Todo bien, gracias. ¿Cómo estás? 
            response_message = "Estoy bien, gracias. ¿En qué estás trabajando hoy?"
        elif language_counts["Spanish"] == 2:
            language_counts["Spanish"] += 1
            # ¡Qué bueno! Necesito ayuda.
            response_message = "¡Perfecto! ¿Algo en mente o exploramos?"
        elif language_counts["Spanish"] == 3:
            language_counts["Spanish"] += 1
            # ¿Puedes ayudarme?
            response_message = "¡Sí! ¿En qué necesitas ayuda?"
        elif language_counts["Spanish"] == 4:
            # Adios
            language_counts["Spanish"] += 1
            response_message = "¡Adiós!"
            # STOP HERE
        else:
            response_message = "¿Qué tal?"
    elif language == "French":
        if language_counts["French"] == 0:
            language_counts["French"] += 1
            # Bonjour
            response_message = "Bonjour ! Comment ça va aujourd'hui?"
        elif language_counts["French"] == 1:
            language_counts["French"] += 1
            # Ca va bien, merci. Et tu, comment ca va?
            response_message = "Je vais très bien, merci! Qu'as-tu prévu de faire aujourd'hui?"
        elif language_counts["French"] == 2:
            language_counts["French"] += 1
            # Aujourd'hui, je vais aller du ski
            response_message = "Excellent! Le ski, c’est toujours une activité formidable. Tu préfères les pistes faciles ou les plus difficiles?"
        elif language_counts["French"] == 3:
            language_counts["French"] += 1
            # Je prefere les pistes tres difficiles! Ou est les collines?
            response_message = "Ah, un amateur de défis! Les collines sont un peu plus loin, mais elles offrent une vue incroyable. Tu es prêt à relever ce défi?"
        elif language_counts["French"] == 4:
            # Oui, je suis pret. Au revoir!
            response_message = "Parfait! Amuse-toi bien et à bientôt!"
    elif language == "Czech":
        if language_counts["Czech"] == 0:
            language_counts["Czech"] += 1
            response_message = "Ahoj!"
        elif language_counts["Czech"] == 1:
            language_counts["Czech"] += 1
            response_message = "Jaký máš plán na dnešní den?"

    # Store the conversation
    # FIX

    if new_conversation or conversation_index is None:
        conversations[language].append([])
        conversation_index = len(conversations[language]) - 1
    conversations[language][conversation_index].append({'user': user_message, 'bot': response_message})
    #conversations[language].append({'user': user_message, 'bot': response_message})

    return jsonify({'response': response_message, 'conversations': conversations[language]})


@app.route('/get_conversation/<language>', methods=['GET'])
def get_conversation(language):
    return jsonify(conversations.get(language, []))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create the tables if they do not exist
    app.run(debug=True)
