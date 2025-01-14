import os
import psycopg2
import secrets

from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='caldb',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.route("/")
def main_page():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_account;')
    users = cur.fetchall()
    cur.execute('SELECT * FROM foods;')
    foods = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        govt_name = request.form['govt_name']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO user_account (username, password, govt_name, weight, height)
            VALUES (%s, crypt(%s, gen_salt('bf')), %s, %s, %s);
        ''', (username, password, govt_name, None, None))
        
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('main_page'))
    return render_template('signup.html')

@app.route('/add-food/', methods=('GET', 'POST'))
def add_food():
    if request.method == 'POST':
        food_name = request.form['food_name']
        brand_name = request.form['brand_name']
        calories = request.form['calories']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO foods (food_name, brand_name, calories, protein, fat, carbs)
            VALUES(%s, %s, %s, %s, %s, %s);
        ''', (food_name, brand_name, calories, protein, fat, carbs))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('main_page'))
    return render_template('addfood.html')

@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT username
            FROM user_account
            WHERE username = %s AND password = crypt(%s, password);
        ''', (username, password))

        user = cur.fetchone()
        if user is not None:
            print("Successful Login!")
            return redirect(url_for('main_page'))
        else:
            print("Invalid Login Information. Check username and password.")
    return render_template('login.html')

