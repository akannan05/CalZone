import os 
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="caldb",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS user_account;')
cur.execute('DROP TABLE IF EXISTS foods;')
cur.execute('DROP TABLE IF EXISTS user_foods;')
cur.execute('CREATE TABLE user_account (user_id serial PRIMARY KEY,'
                                        'username varchar (150) UNIQUE NOT NULL,'
                                        'password varchar (50) NOT NULL,'
                                        'govt_name varchar (80) NOT NULL,'
                                        'weight REAL,'
                                        'height REAL);'
            )
cur.execute('CREATE TABLE foods (food_id serial PRIMARY KEY,'
                                 'food_name varchar (150) UNIQUE NOT NULL,'
                                 'brand_name varchar (200),'
                                 'calories REAL NOT NULL,'
                                 'protein REAL NOT NULL,'
                                 'fat REAL,'
                                 'carbs REAL);'
            )
cur.execute('CREATE TABLE user_foods'
            '(user_id INTEGER REFERENCES user_account(user_id) ON DELETE CASCADE,'
            'food_id INTEGER REFERENCES foods(food_id) ON DELETE CASCADE,'
            'servings INTEGER NOT NULL,'
            'consuption_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'PRIMARY KEY (user_id, food_id));'
            )

conn.commit()

cur.close()
conn.close()
