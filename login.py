# pip install flask flask_bcrypt mysql.connector os flask_login
from flask import Flask, request, redirect, jsonify
from flask_bcrypt import Bcrypt
import os
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Flask Start
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'z::xvs9N`[j):ld.bRx83N)[potFg&yANj.((Nb>bL<CC<SH)/_}2Fi+gV":28i')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Link DataBase
db_config = {
    'host': 'localhost',
    'database': 'lvander_website',
    'user': 'root',
    'passwd': '',
}
db = mysql.connector.connect(**db_config)
cr = db.cursor()


class User(UserMixin):
    def __init__(self, id, email, password, role):
        self.id = id
        self.email = email
        self.password = password
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.email}')"


@login_manager.user_loader
def load_user(user_id):
    cr.execute('select * from `users` where id = %s', (user_id,))
    data = cr.fetchone()
    if data:
        # data[13] is the role column
        return User(data[0], data[3], data[2], data[13])
    return None


# Home Page
# http://127.0.0.1:5000/
@app.route('/')
@login_required
def index():
    return 'hello from home page'


# Log-in Page
# http://127.0.0.1:5000/login?email=omar@gmail.com&password=123
@app.route('/login')
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    if not email or not password:
        return 'you must login', 400
    try:
        cr.execute('select * from `users` where email = %s', (email,))
        data = cr.fetchone()
        if data:
            user = User(data[0], data[3], data[2], data[13])
            if user.check_password(password):
                login_user(user)
                if data[13] == 'user':
                    return redirect('/')
                elif data[13] == 'admin':
                    return redirect('/admin')
                else:
                    return 'error in user select'
            else:
                return 'Wrong Password', 401
        else:
            return 'Wrong username', 401
    except mysql.connector.Error as e:
        return 'Database error', 500


# Admin Page
# http://127.0.0.1:5000/admin
@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin():  # Check if the user is an admin
        return 'hello from admin page'
    else:
        return 'Access denied', 403


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

    if not all([password, email, first_name, last_name, country, city, adress_line1, adress_line2, gender, date_birth, phone]):
        return 'Invalid input', 400
    try:
        cr.execute('select * from `users` where email = %s', (email,))
        data = cr.fetchone()
        if data:
            return f'sorry, {first_name} you already have an account\n', 400
        else:
            hached_pass = bcrypt.generate_password_hash(
                password).decode("utf-8")
            cr.execute('INSERT INTO `users` (password,email,first_name,last_name,country,city,adress_line1,adress_line2,gender,date_birth,phone) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (hached_pass, email, first_name, last_name, country, city, adress_line1, adress_line2, gender, date_birth, phone))
            db.commit()
            return f'user {first_name} added', 201
    except mysql.connector.Error as e:
        return 'Database error', 500

# Logout Page
# http://127.0.0.1:5000/logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# Run server code (development mode)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
