# pip install flask flask_bcrypt mysql.connector os
from flask import Flask, request, redirect, jsonify
from flask_bcrypt import Bcrypt
import os
import mysql.connector


# Flask Start
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
bcrypt = Bcrypt(app)


# Link DataBase
db = mysql.connector.connect(
    host='localhost',
    database='lvander_website',
    user='root',
    passwd='',
)
cr = db.cursor()


# Home Page
# http://127.0.0.1:5000/
@app.route('/')
def index():
    return 'hello from home page'


# Log-in Page
# http://127.0.0.1:5000/login?email=omar@gmail.com&password=123
@app.route('/login')
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    # check valid input
    if not email or not password:
        return 'Invalid input', 400

    # check if user exist
    try:
        cr.execute('select * from `users` where email = %s', (email,))
        data = cr.fetchone()

        # check for password
        if data:
            password_hashed = data[2]
            if bcrypt.check_password_hash(password_hashed, password):
                return redirect('/')
            else:
                return 'Wrong Password', 401
        else:
            return 'Wrong username', 401

    # handling any error (try and except)
    except mysql.connector.Error as e:
        return 'Database error', 500



# Registration Page
#  http://127.0.0.1:5000/registration?username=omar&password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_line1=sgdf&adress_line2=sgdffdd&gender=male&date_birth=1997-05-18&phone=01090220650
@app.route('/registration')
def registration():
    password = request.args.get('password')
    email = request.args.get('email')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    country = request.args.get('country')
    city = request.args.get('city')
    adress_line1 = request.args.get('adress_line1')
    adress_line2 = request.args.get('adress_line2')
    gender = request.args.get('gender')
    date_birth = request.args.get('date_birth')
    phone = request.args.get('phone')
    hached_pass = bcrypt.generate_password_hash(password).decode("utf-8")

    if not all([ password, email, first_name, last_name, country, city, adress_line1, adress_line2, gender, date_birth, phone]):
        return 'Invalid input', 400
    try:
        cr.execute('select * from `users` where email = %s', (email,))
        data = cr.fetchone()
        if data:
            return f'sorry, {first_name} you already have an account\n', 400
        else:
            hached_pass = bcrypt.generate_password_hash(
                password).decode("utf-8")
            cr.execute('INSERT INTO `users` (username,password,email,first_name,last_name,country,city,adress_line1,adress_line2,gender,date_birth,phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (hached_pass, email, first_name, last_name, country, city, adress_line1, adress_line2, gender, date_birth, phone))
            db.commit()
            return f'user {first_name} added', 201
    except mysql.connector.Error as e:
        return 'Database error', 500


# Run server code (development mode)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
