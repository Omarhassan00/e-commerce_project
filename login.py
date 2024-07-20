# pip install flask flask_bcrypt mysql.connector os flask_login
from flask import Flask, request, redirect, jsonify, url_for
from flask_bcrypt import Bcrypt
import os
import mysql.connector
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user
# import uuid
# import smtplib
# from email.message import EmailMessage

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
    'database': 'lavander_website',
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

    # def __init__(self, id, email, password, role, verified):
    #     self.id = id
    #     self.email = email
    #     self.password = password
    #     self.role = role
    #     self.verified = verified
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
        # data[12] is the role column
        return User(data[0], data[4], data[1], data[11])
        # return User(data[0], data[2], data[1], data[12], data[15])
    return None


# Home Page
# http://127.0.0.1:5000/
@app.route('/')
def index():
    cr.execute('SELECT * FROM product LIMIT 10;')
    data = cr.fetchall()
    return jsonify(data)


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
            # user = User(data[0], data[2], data[1], data[12], data[15])
            user = User(data[0], data[4], data[1], data[11])
            if user.check_password(password):
                # if user.verified:
                login_user(user)
                if data[11] == 'user':
                    return redirect('/')
                elif data[11] == 'admin':
                    return redirect('/admin')
                else:
                    return 'error in user select'
                # else:
                #     return 'Please verify your email address', 401
            else:
                return 'Wrong Password', 401
        else:
            return 'Wrong Email', 401
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
        return redirect('/')


# Registration Page
#  http://127.0.0.1:5000/registration?password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_1=sgdf&adress_2=sgdffdd&gender=male&date_birth=1997-05-18&phone=01090220650
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
    # try:
    cr.execute('select * from `users` where email = %s', (email,))
    data = cr.fetchone()
    if data:
        return f'sorry, {first_name} you already have an account\n', 400
    else:
        hached_pass = bcrypt.generate_password_hash(
            password).decode("utf-8")
        # Generate a unique token
        # verification_token = str(uuid.uuid4())
        # Send email verification link
        # send_verification_email(email, verification_token)
        # cr.execute('INSERT INTO `users` (password,email,first_name,last_name,country,city,adress_line1,adress_line2,gender,date_birth,phone,verification_token) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        #            (hached_pass, email, first_name, last_name, country, city, adress_line1, adress_line2, gender, date_birth, phone,verification_token))
        cr.execute('INSERT INTO `users` (password,email,First_name,Last_name,country,adress_1,adress_2,gender,date_birth,phone) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (hached_pass, email, first_name, last_name, country, adress_line1, adress_line2, gender, date_birth, phone))
        db.commit()
        return f'user {first_name} added', 201
    # except mysql.connector.Error as e:
    #     return 'Database error', 500

# def send_verification_email(email, verification_token):
#     # Create a message
#     msg = EmailMessage()
#     msg['Subject'] = 'Verify your email address'
#     msg['From'] = 'omarhassan00123@gmail.com'
#     msg['To'] = email
#     # Create a link with the verification token
#     verification_link = url_for('verify_email', token=verification_token, _external=True)
#     # Add the link to the message body
#     msg.set_content(f'Please click on the following link to verify your email address: {verification_link}')
#     # Send the email using a SMTP server
#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.starttls()
#         smtp.login('yourgmail@gmail.com', 'your password')
#         smtp.send_message(msg)

# @app.route('/verify_email/<token>')
# def verify_email(token):
#     cr.execute('SELECT * FROM `users` WHERE verification_token = %s', (token,))
#     data = cr.fetchone()
#     if data:
#         cr.execute('UPDATE `users` SET verified = 1 WHERE id = %s', (data[0],))
#         db.commit()
#         return 'Email address verified successfully!'
#     else:
#         return 'Invalid verification token', 401


# Logout Page
# http://127.0.0.1:5000/logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# pruduct page
# http://127.0.0.1:5000/products?gender=male


@app.route('/products')
def products():
    prod_gender = request.args.get('gender')
    if prod_gender:
        cr.execute(
            'SELECT * FROM `products` WHERE prod_gender = %s', (prod_gender,))
        gender = cr.fetchall()
        return jsonify(gender)

    else:
        cr.execute('SELECT * FROM `products`')
        prod = cr.fetchall()
        return jsonify(prod)


# card Page
# http://127.0.0.1:5000/card?name=bag
@app.route('/card')
def card():
    name_prod = request.args.get('name')
    cr.execute('SELECT * FROM `products` where name = %s', (name_prod))
    card = cr.fetchone()
    return jsonify(card)


# user information
#  http://127.0.0.1:5000/userinfo?password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_1=sgdf&adress_2=sgdffdd&gender=male&date_birth=1997-05-18&phone=01090220650
@app.route('/userinfo', methods=['GET', 'PUT'])
@login_required
def userinfo():
    if request.method == 'GET':
        cr.execute('SELECT * FROM `users` WHERE id = %s', (current_user.id,))
        data = cr.fetchone()
        return jsonify(data[2:])

    elif request.method == 'PUT':
        password = request.args.get('password')
        user = User(data[0], data[4], data[1], data[11])
        cr.execute('SELECT * FROM `users` WHERE id = %s', (current_user.id,))
        data = cr.fetchone()

        try:
            if user.check_password(password):
                new_password = request.args.get('password')
                new_first_name = request.args.get('first_name')
                new_last_name = request.args.get('last_name')
                new_country = request.args.get('country')
                new_city = request.args.get('city')
                new_adress_line1 = request.args.get('adress_line1')
                new_adress_line2 = request.args.get('adress_line2')
                new_gender = request.args.get('gender')
                new_date_birth = request.args.get('date_birth')
                new_phone = request.args.get('phone')

                if new_password:
                    new_hached_pass = bcrypt.generate_password_hash(
                        new_password).decode("utf-8")
                    cr.execute('UPDATE `users` SET "password" = %s',
                               (new_hached_pass))

                if new_phone:
                    cr.execute('UPDATE `users` SET "phone" = %s', (new_phone))

                if new_last_name:
                    cr.execute('UPDATE `users` SET "last_name" = %s',
                               (new_last_name))

                if new_adress_line1:
                    cr.execute(
                        'UPDATE `users` SET "adress_line1" = %s', (new_adress_line1))

                if new_adress_line2:
                    cr.execute(
                        'UPDATE `users` SET "adress_line2" = %s', (new_adress_line2))

                if new_city:
                    cr.execute('UPDATE `users` SET "city" = %s', (new_city))

                if new_country:
                    cr.execute('UPDATE `users` SET "country" = %s',
                               (new_country))

                if new_date_birth:
                    cr.execute(
                        'UPDATE `users` SET "date_birth" = %s', (new_date_birth))

                if new_gender:
                    cr.execute(
                        'UPDATE `users` SET "gender" = %s', (new_gender))

                if new_first_name:
                    cr.execute(
                        'UPDATE `users` SET "first_name" = %s', (new_first_name))

                db.commit()
                return f'user {new_first_name} updated', 201

            else:
                return f'wrong password', 401
        except mysql.connector.Error as e:
            return 'Database error', 500


# User history
# http://127.0.0.1:5000/history
@app.route('/history')
@login_required
def history():
    try:
        cr.execute(
            'SELECT* from orders INNER JOIN products ON products.id = orders.product_id WHERE user_id = %s', (current_user.id,))
        data = cr.fetchall()
        return jsonify(data), 200
    except mysql.connector.Error as e:
        return 'Database error', 500


# CRAD opration for all users in admin
# http://127.0.0.1:5000/usersadmin
@app.route('/usersadmin', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def usersadmin():
    if current_user.is_admin():
        # show all users
        if request.method == 'GET':
            try:
                cr.execute('SELECT * FROM users')
                data = cr.fetchall()
                return jsonify(data), 200
            except mysql.connector.errors as o:
                return 'Database error', 500
        # add new user
        elif request.method == 'POST':
            try:
                registration()
                return 'new user added'
            except mysql.connector.errors as o:
                return 'Database error', 500
        # update user
        elif request.method == 'PUT':
            try:
                userinfo()
                return 'update this user'
            except mysql.connector.errors as o:
                return 'Database error', 500
        # delete user
        elif request.method == 'DELETE':
            try:
                delete_id = request.args.get('id')
                cr.execute('DELETE FROM users WHERE id = %s', (delete_id,))
                db.commit()
                return 'user deleted'
            except mysql.connector.errors as o:
                return 'Database error', 500


# Run server code (development mode)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
