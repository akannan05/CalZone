import os
import psycopg2
import secrets

from flask import Flask, render_template, request, url_for, redirect, session
from functools import wraps

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='caldb',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def main_page():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_account;')
    users = cur.fetchall()
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
@login_required
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

@app.route('/log-food/', methods=('GET', 'POST'))
@login_required
def log_food():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM foods;')
    foods = cur.fetchall()
    cur.close()
    conn.close()
    if request.method == 'POST':
        user_id = session['user_id']
        food_id = request.form['food_id']
        servings = float(request.form['num_servings'])

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM foods WHERE food_id=%s;', (food_id,))
        
        food_info = cur.fetchone()
        
        log_calories = float(food_info[3])*servings
        log_protein = float(food_info[4])*servings
        log_fat = float(food_info[5])*servings
        log_carbs = float(food_info[6])*servings

        cur.execute('''
            INSERT INTO user_foods (user_id, food_id, servings, calories, protein, fat,
            carbs)
            VALUES(%s, %s, %s, %s, %s, %s, %s);
        ''', (user_id, food_id, servings, log_calories, log_protein, log_fat, log_carbs))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('main_page'))
    return render_template('logfood.html', foods=foods)

@app.route('/view-log/')
@login_required
def view_log():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_foods WHERE user_id=%s;', (user_id,))
    logged_foods = cur.fetchall()

    logged_food_ids = []
    for row in logged_foods:
        logged_food_ids.append(row[1])

    cur.execute('SELECT * FROM foods WHERE food_id IN %s;', (tuple(logged_food_ids),))
    food_info = cur.fetchall()

    food_info_dict = {food[0]: food for food in food_info} 

    cur.close()
    conn.close()
    return render_template('viewlog.html', logged_foods=logged_foods,
                           food_info_dict=food_info_dict)

@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT user_id
            FROM user_account
            WHERE username = %s AND password = crypt(%s, password);
        ''', (username, password))

        user_id = cur.fetchone()
        if user_id is not None:
            session['user_id'] = user_id[0]
            return redirect(url_for('main_page'))
        else:
            print("Invalid Login Information. Check username and password.")
    return render_template('login.html')

@app.route('/logout/', methods=('GET', 'POST'))
@login_required
def logout():
    if request.method == 'POST':
        session.pop('user_id', None)
        return redirect(url_for('login'))
        
