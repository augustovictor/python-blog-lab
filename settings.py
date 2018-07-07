import os

SECRET_KEY = 'OUR-SECRET'
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'flask-db'
DB_HOST = '127.0.0.1'
DB_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=True
UPLOADED_IMAGES_DEST = '/Users/victoraweb/python-blog-lab/static/img'
UPLOADED_IMAGES_URL = '/static/img'