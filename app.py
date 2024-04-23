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
