from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from config import UPLOAD_FOLDER, GALLERY_FOLDER, UPLOADS_ROUTE, GALLERY_FILES_ROUTE
from db import init_db
from routes.menu import register_menu_routes
from routes.gallery import register_gallery_routes

# ایجاد پوشه‌ها (اگر وجود نداشتند)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GALLERY_FOLDER, exist_ok=True)

# ساخت اپلیکیشن Flask
app = Flask(__name__)
CORS(app, supports_credentials=True)

# مقداردهی اولیه دیتابیس
init_db()

# ثبت مسیرهای مربوط به منو و گالری
register_menu_routes(app)
register_gallery_routes(app)

# مسیر نمایش فایل‌های آپلود شده
@app.route(f"{UPLOADS_ROUTE}/<filename>")
def serve_menu_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route(f"{GALLERY_FILES_ROUTE}/<filename>")
def serve_gallery_image(filename):
    return send_from_directory(GALLERY_FOLDER, filename)

# فقط برای اجرای محلی
if __name__ == '__main__':
    app.run(debug=True)
