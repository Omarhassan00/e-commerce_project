from app import *
from database import cr, db
from models import user
from flask import request, redirect, jsonify, Blueprint
import mysql.connector
from flask_login import current_user, login_required, logout_user
import models.cart


# def blueprint
bp = Blueprint('auth', __name__)


# Logout Page
# http://127.0.0.1:5000/logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# user information
# http://127.0.0.1:5000/userinfo?password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_1=sgdf&adress_2=sgdffdd&gender=male&date_birth=1997-05-18&phone=01090220650
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
            'SELECT * from orders INNER JOIN products ON products.id = orders.product_id WHERE user_id = %s', (current_user.id,))
        data = cr.fetchall()
        return jsonify(data), 200
    except mysql.connector.Error as e:
        return 'Database error', 500


# catr CRAD opration
# http://127.0.0.1:5000/cart
@bp.route('/cart', methods=['GET', 'POST', 'DELETE'])
@login_required
def cart():
    # show cart
    if request.method == 'GET':
        return models.cart.show_cart(current_user.id,)

    # add to cart
    elif request.method == 'POST':
        product_id = request.args.get('product_id')
        quantity = request.args.get('amount_product')
        return models.cart.add_product(product_id, current_user.id, quantity,)

    # delete from cart
    elif request.method == 'DELETE':
        return models.cart.delete_oneproduct(current_user.id,)

    else:
        return 'error input', 500


# order submit
# http://127.0.0.1:5000/submit
@bp.route('/submit', methods=['GET'])
@login_required
def submit():
    # get data from request
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    address = request.args.get('address')
    price = request.args.get('price')
    total = request.args.get('total')


    # add data to database
    cr.execute('INSERT INTO orders (user_id	,product_id	,quantity ,total_amount ,address ,price) VALUES (%s , %s , %s, %s , %s , %s)',
            (current_user.id, product_id, quantity, total, address, price))
    db.commit()

    # delete old cart from all product
    models.cart.delete_cart(current_user.id,)
    return 'order saved'