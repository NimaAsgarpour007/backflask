from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from config import UPLOAD_FOLDER, GALLERY_FOLDER, UPLOADS_ROUTE, GALLERY_FILES_ROUTE
from db import init_db
from routes.menu import register_menu_routes
from routes.gallery import register_gallery_routes

# ایجاد پوشه‌ها
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GALLERY_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app, supports_credentials=True)

# مقداردهی اولیه دیتابیس
init_db()

# ثبت مسیرها
register_menu_routes(app)
register_gallery_routes(app)

# مسیرهای سرو فایل
@app.route(f"{UPLOADS_ROUTE}/<filename>")
def serve_menu_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route(f"{GALLERY_FILES_ROUTE}/<filename>")
def serve_gallery_image(filename):
    return send_from_directory(GALLERY_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
