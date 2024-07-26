from app import *
from database import cr
from models import user , product
from flask import request, jsonify, Blueprint 


bp2 = Blueprint('main', __name__)
# pruduct page
# http://127.0.0.1:5000/products?gender=male
@bp2.route('/products')
def products():
    # filter with gender
    prod_gender = request.args.get('gender')
    if prod_gender in ['male', 'female']:
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
@bp2.route('/card')
def card():
    name_prod = request.args.get('name')
    cr.execute('SELECT * FROM `products` WHERE name = %s', (name_prod,))
    card = cr.fetchall()
    return jsonify(card)

# Registration Page
# http://127.0.0.1:5000/registration?password=123&email=omarhassan&first_name=oar&last_name=hassan&country=egypt&city=suez&adress_1=sgdf&adress_2=sgdffdd&gender=male&date_birth=1997-05-18&phone=01090220650
@bp2.route('/registration')
def registration():
    return user.User.user_registration()

# Home Page
# http://127.0.0.1:5000/
@bp2.route('/')
def index():
    cr.execute('SELECT * FROM `products` ORDER BY `products`.`sales` DESC')
    data = cr.fetchall()
    return jsonify(data)


# Log-in Page
# http://127.0.0.1:5000/login?email=omar@gmail.com&password=123
@bp2.route('/login')
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    if not email or not password:
        return 'you must login', 400
    return user.User.user_login(email,password)
