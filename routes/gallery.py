from flask import request, jsonify, send_from_directory
import os
from db import get_db_connection
from config import GALLERY_ROUTE, GALLERY_FOLDER

def register_gallery_routes(app):
    @app.route(GALLERY_ROUTE, methods=['POST'])
    def upload_gallery_image():
        image = request.files.get('image')
        title = request.form.get('title')
        description = request.form.get('description')

        if not image or not title or not description:
            return jsonify({"error": "همه فیلدها الزامی هستند"}), 400

        image_path = os.path.join(GALLERY_FOLDER, image.filename)
        image.save(image_path)
        image_url = f"/gallery_files/{image.filename}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO gallery (title, description, image_url) VALUES (?, ?, ?)',
            (title, description, image_url)
        )
        conn.commit()
        gallery_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "id": gallery_id,
            "title": title,
            "description": description,
            "image_url": image_url
        }), 201

    @app.route(GALLERY_ROUTE, methods=['GET'])
    def get_gallery():
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM gallery').fetchall()
        conn.close()
        return jsonify([dict(item) for item in items])
