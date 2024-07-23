<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
import os
import logging
from flask import jsonify
app = Flask(__name__)
def create_user_table():
    try:
        connection = sqlite3.connect('mini.db')
        cursor = connection.cursor()

        connection.commit()
        connection.close()
        print("Database connected and User table created successfully.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Create the User table before running the app
create_user_table()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        name = request.form['username']
        gmail=request.form['gmail']
        password = request.form['password']


        # Check if the user exists in the User table
        try:
            connection = sqlite3.connect('mini.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM login WHERE name = ? AND pass = ?', (name, password))
            user = cursor.fetchone()
            connection.close()

            if user:
                return redirect(url_for('dashboard')) 
            else:
               return "Login failed. Please login again <a href='" + url_for('index') + "'>login_again</a>."
        except Exception as e:
            print(f"Error checking user in the database: {e}")

    return render_template('user.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['username']
        gmail=request.form['gmail']
        password = request.form['password']

     
        try:
            connection = sqlite3.connect('mini.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO login (name, email ,pass) VALUES (?,?, ?)', (name,gmail, password))
            connection.commit()
            connection.close()
            print("User added to the database.")
            return redirect(url_for('user')) 
        except Exception as e:
            print(f"Error adding user to the database: {e}")

    return render_template('registration.html')
@app.route('/l_registration', methods=['GET', 'POST'])
def l_registration():
    if request.method == 'POST':
        username = request.form['username']
        gmail = request.form['gmail']
        password = request.form['password']
        phone_number = request.form['phno']
        enrollment_number = request.form['enrollment']
        specialization = request.form['specialization']

     
        try:
            connection = sqlite3.connect('mini.db')
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO lawyer (name1, email1, pass1, phno, enrollment, specialization)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, gmail, password, phone_number, enrollment_number, specialization))
            connection.commit()
            connection.close()
            print("Lawyer data inserted into the database.")
            return redirect(url_for('index')) 
        except Exception as e:
            print(f"Error adding lawyer data to the database: {e}")

    return render_template('l_registration.html')    
@app.route('/lawyer', methods=['POST','GET'])
def lawyer():
    if request.method == 'POST':
        username = request.form['name1']
        gmail = request.form['gmail1']
        password = request.form['pass1']

        try:
            connection = sqlite3.connect('mini.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM lawyer WHERE name1 = ? AND email1 = ? AND pass1 = ?', (username, gmail, password))
            lawyer = cursor.fetchone()
            connection.close()

            if lawyer:
               
                return redirect(url_for('dashboard'))
            else:
                return "Login failed. Please check your credentials and try again."
        except Exception as e:
            print(f"Error checking user in the database: {e}")

    return render_template('lawyer.html')    


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')    

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import logging
import easyocr
import numpy as np
import spacy
from PIL import Image
import io
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.spatial.distance import cosine as cosine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Ensure the upload folders exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'certificates'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'id_proofs'), exist_ok=True)

# Function to create database connection
def get_db_connection():
    conn = sqlite3.connect('mini.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create tables
def create_tables():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                pass TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lawyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name1 TEXT,
                email1 TEXT,
                pass1 TEXT,
                phno TEXT,
                enrollment TEXT,
                specialization TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                specialization TEXT,
                education TEXT,
                exp INTEGER,
                lang TEXT,
                loc TEXT,
                bio TEXT,
                pic TEXT,
                cert TEXT,
                proof TEXT,
                num TEXT
            )
        ''')
        connection.commit()
        connection.close()
        print("Database connected and tables created successfully.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Create the necessary tables before running the app
create_tables()

# Route to display the index page
@app.route('/')
def index():
    return render_template('index.html')

# User login route
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        name = request.form['username']
        gmail = request.form['gmail']
        password = request.form['password']

        # Check if the user exists in the login table
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM login WHERE name = ? AND email = ? AND pass = ?', (name, gmail, password))
            user = cursor.fetchone()
            connection.close()

            if user:
                return redirect(url_for('dashboard',user_id=user[0]))
            else:
                return "Login failed. Please login again <a href='" + url_for('index') + "'>login_again</a>."
        except Exception as e:
            print(f"Error checking user in the database: {e}")

    return render_template('user.html')

# User registration route
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['username']
        gmail = request.form['gmail']
        password = request.form['password']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO login (name, email, pass) VALUES (?, ?, ?)', (name, gmail, password))
            connection.commit()
            connection.close()
            return redirect(url_for('user'))
        except Exception as e:
            print(f"Error adding user to the database: {e}")

    return render_template('registration.html')

# Lawyer registration route
@app.route('/l_registration', methods=['GET', 'POST'])
def l_registration():
    if request.method == 'POST':
        username = request.form['username']
        gmail = request.form['gmail']
        password = request.form['password']
        phone_number = request.form['phno']
        enrollment_number = request.form['enrollment']
        specialization = request.form['specialization']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO lawyer (name1, email1, pass1, phno, enrollment, specialization)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, gmail, password, phone_number, enrollment_number, specialization))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error adding lawyer data to the database: {e}")

    return render_template('l_registration.html')

# Lawyer login route
@app.route('/lawyer', methods=['POST', 'GET'])
def lawyer():
    if request.method == 'POST':
        username = request.form['name1']
        gmail = request.form['gmail1']
        password = request.form['pass1']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM lawyer WHERE name1 = ? AND email1 = ? AND pass1 = ?', (username, gmail, password))
            lawyer = cursor.fetchone()
            connection.close()

            if lawyer:
                return redirect(url_for('dashboard',user_id=lawyer[0]))
            else:
                return "Login failed. Please check your credentials and try again."
        except Exception as e:
            print(f"Error checking user in the database: {e}")

    return render_template('lawyer.html')

# OCR and text summarization setup
reader = easyocr.Reader(['en'])
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')

# Function to extract text from file
def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.replace("\n", "")
        return text
    except Exception as e:
        return str(e)

# Function to read article
def read_article(text):
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence.replace("[^a-zA-Z0-9]", " ")
    return sentences

# Function to calculate sentence similarity
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        if not w in stopwords:
            vector1[all_words.index(w)] += 1

    for w in sent2:
        if not w in stopwords:
            vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

# Function to build similarity matrix
def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 != idx2:
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

# Function to generate summary
def generate_summary(text, top_n):
    stop_words = stopwords.words('english')
    summarize_text = []

    sentences = read_article(text)
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    for i in range(top_n):
        summarize_text.append(ranked_sentences[i][1])

    return " ".join(summarize_text), len(sentences)

# Route for uploading text file and performing text summarization
@app.route('/process_text_file', methods=['POST'])
def process_text_file():
    if 'file' not in request.files:
        return render_template('ocr.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('ocr.html', error='No selected file')

    num_sentences = int(request.form['num_sentences'])
    if file:
        text = file.read().decode('utf-8')
        summary_text, total_sentences = generate_summary(text, num_sentences)
        return render_template('ocr.html', text=text, summary=summary_text)

# Route for lawyer portal data submission
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'certificates'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'id_proofs'), exist_ok=True)
def get_db_connection():
    conn = sqlite3.connect('mini.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/lawcon', methods=['GET', 'POST'])
def lawcon():
    if request.method == 'POST':
        specialization = request.form['specialization']
        education = request.form['education']
        experience = request.form['experience']
        languages = request.form['languages']
        location = request.form['location']
        bio = request.form['bio']
        bar_number = request.form['bar-number']

        profile_pic = request.files['profile-pic']
        certificates = request.files.getlist('certificates')
        id_proof = request.files['id-proof']

        profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics', profile_pic.filename)
        profile_pic.save(profile_pic_path)

        certificate_paths = []
        for certificate in certificates:
            certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], 'certificates', certificate.filename)
            certificate.save(certificate_path)
            certificate_paths.append(certificate_path)

        id_proof_path = os.path.join(app.config['UPLOAD_FOLDER'], 'id_proofs', id_proof.filename)
        id_proof.save(id_proof_path)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO portal (specialization, education, exp, lang, loc, bio, pic, cert, proof, num)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (specialization, education, experience, languages, location, bio, profile_pic_path, ';'.join(certificate_paths), id_proof_path, bar_number))
        connection.commit()
        connection.close()

        return redirect(url_for('lawcon'))
    return render_template('lawcon.html')

@app.route('/lawyers')
def lawyers():
    # Check if the user is authenticated
    if 'user_id' not in request.args:
        return redirect(url_for('index'))

    # Fetch user's ID from the URL parameter
    user_id = request.args.get('user_id')

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch user's details from login table
    cursor.execute('SELECT name, email FROM login WHERE id = ?', (user_id,))
    user_details = cursor.fetchone()

    if user_details:
        # Fetch lawyers' profiles matching user's criteria
        cursor.execute('''
    SELECT lawyer.name1, lawyer.email1, lawyer.phno, lawyer.specialization, portal.education, portal.lang, portal.loc, portal.bio, portal.pic, portal.cert 
    FROM lawyer 
    JOIN portal ON lawyer.id1 = portal.id
''')

        lawyers_profiles = cursor.fetchall()

        connection.close()

        return render_template('lawyers.html', user_details=user_details, lawyers_profiles=lawyers_profiles)
    else:
        connection.close()
        return redirect(url_for('index'))
        
# Route for OCR page
@app.route('/ocr')
def ocr():
    return render_template('ocr.html')

# Route for dashboard
@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM login WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    connection.close()

    # Check if the user exists
    if user:
        username = user['name']
        return render_template('dashboard.html', username=username, user_id=user_id)
    else:
        return "User not found"

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> a305c67 (Your commit message)
