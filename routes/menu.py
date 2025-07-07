from flask import request, jsonify, send_from_directory
import os
from db import get_db_connection
from config import MENU_ROUTE, UPLOAD_FOLDER

def register_menu_routes(app):
    @app.route(MENU_ROUTE, methods=['POST'])
    def add_menu_item():
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files.get('image')

        if not all([name, description, price, image]):
            return jsonify({"error": "لطفا تمام فیلدها را وارد کنید"}), 400

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)
        image_url = f"/uploads/{image.filename}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO menu (name, description, price, image_url) VALUES (?, ?, ?, ?)',
            (name, description, float(price), image_url)
        )
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "id": item_id,
            "name": name,
            "description": description,
            "price": float(price),
            "image_url": image_url
        }), 201

    @app.route(MENU_ROUTE, methods=['GET'])
    def get_menu():
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM menu').fetchall()
        conn.close()
        return jsonify([dict(item) for item in items])

    @app.route(f"{MENU_ROUTE}/<int:item_id>", methods=['DELETE'])
    def delete_menu_item(item_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM menu WHERE id = ?', (item_id,))
        conn.commit()
        changes = cursor.rowcount
        conn.close()

        if changes == 0:
            return jsonify({"error": "آیتم پیدا نشد"}), 404
        return jsonify({"message": "آیتم با موفقیت حذف شد"}), 200

    @app.route(f"{MENU_ROUTE}/<int:item_id>", methods=['PUT'])
    def update_menu_item(item_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        item = conn.execute('SELECT * FROM menu WHERE id = ?', (item_id,)).fetchone()
        if not item:
            conn.close()
            return jsonify({"error": "آیتم پیدا نشد"}), 404

        name = request.form.get('name', item['name'])
        description = request.form.get('description', item['description'])
        price = request.form.get('price', item['price'])
        image = request.files.get('image')

        image_url = item['image_url']
        if image:
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)
            image_url = f"/uploads/{image.filename}"

        cursor.execute('''
            UPDATE menu SET name = ?, description = ?, price = ?, image_url = ?
            WHERE id = ?
        ''', (name, description, float(price), image_url, item_id))
        conn.commit()
        conn.close()

        return jsonify({
            "id": item_id,
            "name": name,
            "description": description,
            "price": float(price),
            "image_url": image_url
        }), 200
