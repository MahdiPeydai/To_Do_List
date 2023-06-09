import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ACTIVITY_AVATAR_ALLOWED_EXTENSIONS = os.getenv('ACTIVITY_AVATAR_ALLOWED_EXTENSIONS')
ACTIVITY_AVATAR_UPLOAD_FOLDER = os.getenv('ACTIVITY_AVATAR_UPLOAD_FOLDER')
