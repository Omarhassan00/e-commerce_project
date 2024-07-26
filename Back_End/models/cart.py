from database import cr, db
from app import *
from flask import request, jsonify


# add new product
'''used in when user add a new product to his cart or increase an exists product'''


def add_product(product_id, user_id, amount):
    try:
        cr.execute(
            "SELECT * from carts WHERE user_id = %s AND product_id = %s", (user_id, product_id,))
        result = cr.fetchall()
        if result:
            cr.execute("UPDATE carts SET amount_product = amount_product + %s WHERE user_id = %s AND product_id = %s",
                       (amount, user_id, product_id,))
            db.commit()
            return 'product added'
        else:
            cr.execute("INSERT INTO carts (product_id, user_id, amount_product) VALUES (%s,%s,%s)",
                       (product_id, user_id, amount,))
            db.commit()
            return 'product added'
    except:
        return 'database error'


# show all cart product
'''show all product in user cart'''


def show_cart(user_id):
    try:
        cr.execute(
            "SELECT * from carts INNER JOIN products ON products.id = carts.product_id WHERE user_id = %s", (user_id,))
        data = cr.fetchall()
        return jsonify(data)
    except:
        return 'database error'


# delete product
'''with delete method to decrease or delete one product from cart'''


def delete_oneproduct(user_id):
    product_id = request.args.get("productid")
    amount = request.args.get("amount")
    try:
        cr.execute(
            "SELECT * from carts WHERE user_id = %s AND product_id = %s", (user_id, product_id,))
        result = cr.fetchall()
        if result:
            if amount:
                cr.execute("UPDATE carts SET amount_product = amount_product - %s WHERE user_id = %s and product_id = %s",
                           (amount, user_id, product_id,))
                db.commit()
                return 'product deleted'
            else:
                cr.execute(
                    "DELETE FROM carts WHERE user_id = %s AND product_id = %s", (user_id, product_id,))
                db.commit()
                return 'product deleted'
        else:
            return 'product not found'
    except:
        return 'database error'


# delete all cart product
'''to delete all product from cart when the user done the payment procces'''


def delete_cart(user_id):
    try:
        cr.execute("DELETE FROM carts WHERE user_id = %s", (user_id,))
        db.commit()
        return 'cart deleted'
    except:
        return 'database error'