import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
GALLERY_FOLDER = os.path.join(BASE_DIR, 'gallery')
DATABASE = os.path.join(BASE_DIR, 'app.db')

# API Routes
MENU_ROUTE = '/menu'
GALLERY_ROUTE = '/gallery'
UPLOADS_ROUTE = '/uploads'
GALLERY_FILES_ROUTE = '/gallery_files'
