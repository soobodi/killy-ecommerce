import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Clave secreta
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/"
        f"{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 2,        # máximo de conexiones activas
    'max_overflow': 0,     # conexiones extras que se pueden crear sobre el pool
    'pool_recycle': 280,   # segundos tras los cuales se recicla la conexión
}

    # -------------------------------------------------
    # Configuración para subida de imágenes
    # -------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static',
        'img',
        'productos'
    )

    MAX_CONTENT_LENGTH = 3 * 1024 * 1024   # 3 MB

    ALLOWED_EXTENSIONS = {
        'jpg',
        'jpeg',
        'webp'
    }
