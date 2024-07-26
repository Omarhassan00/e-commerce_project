from app import *
from database import cr , db
from models import user, product
from flask import request, redirect, jsonify, Blueprint
import mysql.connector
from flask_login import current_user, login_required


# def blueprint
bp = Blueprint('admin', __name__)


# Main Admin Page
# http://127.0.0.1:5000/admin
@bp.route('/admin')
@login_required
def admin():
    if current_user.is_admin():  # Check if the user is an admin
        cr.execute('SELECT First_name FROM users WHERE id = %s',(current_user.id,))
        data = cr.fetchall()
        return jsonify(data)
    else:
        return redirect('/')


# CRAD opration for users in admin
# http://127.0.0.1:5000/admin/user
@bp.route('/admin/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def usersadmin():
    if current_user.is_admin():

        # show all users
        if request.method == 'GET':
            return user.User.show_all_users()

        # add new user
        elif request.method == 'POST':
            try:
                return user.User.user_registration()
                
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

    else:
        return redirect('/')



# CRAD opration for product in admin
# http://127.0.0.1:5000/admin/product
@bp.route('/admin/product', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def product_admin():
    if current_user.is_admin():

        # show all product
        if request.method == 'GET':
            return product.product.show_all_product()


        # add new product
        elif request.method == 'POST':
            try:
                return product.product.new_product()
            except mysql.connector.errors as o:
                return 'Database error', 500


        # update product info
        elif request.method == 'PUT':
            try:
                return product.product.update_product()
            except mysql.connector.errors as o:
                return 'Database error', 500


        # delete any product
        elif request.method == 'DELETE':
            return product.product.delete_product()
    else:
        return redirect('/')


# show all inventory
# http://127.0.0.1:5000/admin/inventory
@bp.route('/admin/inventory',methods=['GET', 'PUT'])
@login_required
def inventory_admin():
    if current_user.is_admin():
        if request.method == 'GET':
            cr.execute('SELECT id , name, stock FROM products')
            data = cr.fetchall()
            return jsonify(data)
        

        # update stock
        elif request.method == 'PUT':
            try:
                new_stock = request.args.get('stock')
                product_id = request.args.get('id')
                cr.execute('UPDATE products SET stock = %s WHERE id = %s', (new_stock , product_id ,))
                db.commit()
                return 'Updated', 200
            except mysql.connector.errors as o:
                return 'Database error', 500
    else:
        return redirect('/')


# show salse
# http://127.0.0.1:5000/admin/sales
@bp.route('/admin/sales')
@login_required
def sales_admin():
    if current_user.is_admin():
        cr.execute('SELECT id, name, sales FROM products')
        data = cr.fetchall()
        return jsonify(data)
    else:
        return redirect('/')


# show membership opration
# http://127.0.0.1:5000/admin/membership
@bp.route('/admin/membership',methods=['GET', 'PUT'])
@login_required
def membership_admin():
    if current_user.is_admin():
        if request.method == 'GET':
            return user.User.show_membership()
        
        
        # update membership role
        elif request.method == 'PUT':
            return user.User.update_membership()
        
        else:
            return 'wrong request'

    else:
        return redirect('/')