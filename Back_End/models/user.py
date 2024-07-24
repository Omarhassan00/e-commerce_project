from database import cr , db
from app import *
from flask_login import UserMixin , login_user
from flask import request, jsonify
import mysql.connector
from flask import redirect


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




    def show_all_users():
            try:
                cr.execute('SELECT * FROM users')
                data = cr.fetchall()
                return jsonify(data), 200
            except mysql.connector.errors as o:
                return 'Database error', 500

    def delete_user():
        try:
            delete_id = request.args.get('id')
            cr.execute('DELETE FROM `users` WHERE id = %s', (delete_id,))
            db.commit()
            return 'user deleted'
        except mysql.connector.errors as o:
            return 'Database error', 500

    def user_info(id):

        cr.execute('SELECT * FROM `users` WHERE id = %s', (id,))
        data = cr.fetchone()
        return jsonify(data[2:])

    def update_info(id):
        password = request.args.get('password')
        user = User(data[0], data[4], data[1], data[11])
        cr.execute('SELECT * FROM `users` WHERE id = %s', (id,))
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
                    cr.execute('UPDATE `users` SET "phone" = %s', (new_phone,))

                if new_last_name:
                    cr.execute('UPDATE `users` SET "last_name" = %s',
                               (new_last_name,))

                if new_adress_line1:
                    cr.execute(
                        'UPDATE `users` SET "adress_line1" = %s', (new_adress_line1,))

                if new_adress_line2:
                    cr.execute(
                        'UPDATE `users` SET "adress_line2" = %s', (new_adress_line2,))

                if new_city:
                    cr.execute('UPDATE `users` SET "city" = %s', (new_city,))

                if new_country:
                    cr.execute('UPDATE `users` SET "country" = %s',
                               (new_country,))

                if new_date_birth:
                    cr.execute(
                        'UPDATE `users` SET "date_birth" = %s', (new_date_birth,))

                if new_gender:
                    cr.execute(
                        'UPDATE `users` SET "gender" = %s', (new_gender,))

                if new_first_name:
                    cr.execute(
                        'UPDATE `users` SET "first_name" = %s', (new_first_name,))

                db.commit()
                return f'user {new_first_name,} updated', 201

            else:
                return f'wrong password', 401
        except mysql.connector.Error as e:
            return 'Database error', 500

    def user_login(email,password):

        try:
            cr.execute('select * from `users` where email = %s', (email,))
            data = cr.fetchone()
            if data:
                # user = User(data[0], data[2], data[1], data[12], data[15])
                user = User(data[0], data[4], data[1], data[11])
                if user.check_password(password):
                    login_user(user)
                    # if user.verified:
                    if data[11] == 'user':
                        return 'hello from home'
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

    def user_registration():
        password = request.args.get('password')
        email = request.args.get('email')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        country = request.args.get('country')
        city = request.args.get('city')
        adress_line1 = request.args.get('adress_1')
        adress_line2 = request.args.get('adress_2')
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
            cr.execute('INSERT INTO `users` (password,email,First_name,Last_name,country,adress_1,adress_2,gender,date_birth,phone) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (hached_pass, email, first_name, last_name, country, adress_line1, adress_line2, gender, date_birth, phone))
            db.commit()
            return f'user {first_name} added', 201
    # except mysql.connector.Error as e: