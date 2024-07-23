from database import cr, db
from flask import request, jsonify
import mysql.connector


class product():

    def show_all_product():
            try:
                cr.execute('SELECT * FROM products')
                data = cr.fetchall()
                return jsonify(data), 200
            except mysql.connector.errors as o:
                return 'Database error', 500

    def product_info(id):

        cr.execute('SELECT * FROM `products` WHERE id = %s', (id,))
        data = cr.fetchone()
        return jsonify(data)

    def delete_product():
        try:
            delete_id = request.args.get('id')
            cr.execute('DELETE FROM products WHERE id = %s', (delete_id,))
            db.commit()
            return 'product deleted'
        except mysql.connector.errors as o:
            return 'Database error', 500

    def update_product(id):

        cr.execute('SELECT * FROM `products` WHERE id = %s', (id,))
        data = cr.fetchone()

        try:
            if data:
                new_price = request.args.get('price')
                new_name = request.args.get('name')
                new_discount = request.args.get('discount')
                new_image = request.args.get('image')
                new_stock = request.args.get('stock')
                new_gender = request.args.get('gender')
                new_offer = request.args.get('offer')
                new_docs = request.args.get('discription')

                if new_price:
                    cr.execute('UPDATE `products` SET "price" = %s',
                               (new_price,))

                if new_name:
                    cr.execute('UPDATE `products` SET "name" = %s', (new_name,))

                if new_discount:
                    cr.execute('UPDATE `products` SET "discount" = %s',
                               (new_discount,))

                if new_image:
                    cr.execute(
                        'UPDATE `products` SET "image" = %s', (new_image,))

                if new_stock:
                    cr.execute(
                        'UPDATE `products` SET "stock" = %s', (new_stock,))

                if new_offer:
                    cr.execute(
                        'UPDATE `products` SET "offer_price" = %s', (new_offer,))

                if new_docs:
                    cr.execute('UPDATE `products` SET "discription" = %s',
                               (new_docs,))

                if new_gender:
                    cr.execute(
                        'UPDATE `products` SET "gender" = %s', (new_gender,))

                db.commit()
                return f'product updated', 201

            else:
                return f'wrong product id', 401
        except mysql.connector.Error as e:
            return 'Database error', 500

    def new_product():
        price = request.args.get('price')
        name = request.args.get('name')
        discount = request.args.get('discount')
        image = request.args.get('image')
        stock = request.args.get('stock')
        gender = request.args.get('gender')
        offer = request.args.get('offer')
        docs = request.args.get('discription')

        if not all([price, name, discount, image, stock, gender, offer, docs]):
            return 'Invalid input', 400
        # try:
        cr.execute('select * from `products` where name = %s', (name,))
        data = cr.fetchone()
        if data:
            return f'sorry, {name} already exist\n', 400
        else:
            cr.execute('INSERT INTO `products` (price,name,discount,image,stock,offer,discription,gender) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)',
                       (price, name, discount, image, stock, gender, offer, docs))
            db.commit()
            return f'product {name} added', 201
    # except mysql.connector.Error as e:
