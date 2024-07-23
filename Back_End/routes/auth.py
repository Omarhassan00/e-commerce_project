from app import *
from database import cr
from models import user, product
from flask import request, redirect, jsonify, Blueprint
import mysql.connector
from flask_login import current_user, login_required, logout_user


# def blueprint
bp = Blueprint('auth', __name__)

# Admin Page
# http://127.0.0.1:5000/admin


@bp.route('/admin')
@login_required
def admin():
    if current_user.is_admin():  # Check if the user is an admin
        return 'hello from admin page'
    else:
        return redirect('/')

# Logout Page
# http://127.0.0.1:5000/logout


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# user information
#  http://127.0.0.1:5000/userinfo?password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_1=sgdf&adress_2=sgdffdd&gender=male&date_birth=1997-05-18&phone=01090220650
@bp.route('/userinfo', methods=['GET', 'PUT'])
@login_required
def userinfo():
    # show user info
    if request.method == 'GET':
        return user.User.user_info(current_user.id,)
    # update user info
    elif request.method == 'PUT':
        return user.User.update_info(current_user.id,)

# User history
# http://127.0.0.1:5000/history


@bp.route('/history')
@login_required
def history():
    try:
        cr.execute(
            'SELECT* from orders INNER JOIN products ON products.id = orders.product_id WHERE user_id = %s', (current_user.id,))
        data = cr.fetchall()
        return jsonify(data), 200
    except mysql.connector.Error as e:
        return 'Database error', 500


# CRAD opration for users in admin
# http://127.0.0.1:5000/admin/user
@bp.route('/admin/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def usersadmin():
    # if current_user.is_admin():

        # show all users
        if request.method == 'GET':
            return user.User.show_all_users()

        # add new user
        elif request.method == 'POST':
            try:
                return user.User.user_registration()
                return 'new user added'
            except mysql.connector.errors as o:
                return 'Database error', 500

        # update user
        elif request.method == 'PUT':
            try:
                return user.User.user_info()
            except mysql.connector.errors as o:
                return 'Database error', 500

        # delete user
        elif request.method == 'DELETE':
            return user.User.delete_user()

    # else:
    #     return 'You are not authorized to access this page', 403


# CRAD opration for product in admin
# http://127.0.0.1:5000/admin/product

@bp.route('/admin/product', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
def product_admin():
    # if current_user.is_admin():
        if request.method == 'GET':
            return product.product.show_all_product()

        elif request.method == 'POST':
            try:
                return product.product.new_product()
            except mysql.connector.errors as o:
                return 'Database error', 500

        elif request.method == 'PUT':
            try:
                return product.product.update_product()
            except mysql.connector.errors as o:
                return 'Database error', 500

        elif request.method == 'DELETE':
            return product.product.delete_product()
    # else:
    #     return 'You are not authorized to access this page', 403
