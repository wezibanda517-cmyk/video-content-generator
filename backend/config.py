import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_RATE_LIMIT = int(os.getenv('OPENAI_RATE_LIMIT', '3'))
    
    # Facebook
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
    FACEBOOK_API_VERSION = os.getenv('FACEBOOK_API_VERSION', 'v18.0')
    FACEBOOK_RATE_LIMIT = int(os.getenv('FACEBOOK_RATE_LIMIT', '10'))
    
    # Video Configuration
    VIDEO_OUTPUT_RESOLUTION = os.getenv('VIDEO_OUTPUT_RESOLUTION', '1920x1080')
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', '30'))
    VIDEO_CODEC = os.getenv('VIDEO_CODEC', 'libx264')
    VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', 'high')
    MAX_VIDEO_DURATION = int(os.getenv('MAX_VIDEO_DURATION', '600'))  # 10 minutes
    
    # Storage
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', './output')
    LOGS_FOLDER = './logs'
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '5000000000'))  # 5GB
    
    # Subtitle Configuration
    SUBTITLE_LANGUAGE = os.getenv('SUBTITLE_LANGUAGE', 'en')
    SUBTITLE_FONT_SIZE = int(os.getenv('SUBTITLE_FONT_SIZE', '24'))
    SUBTITLE_COLOR = os.getenv('SUBTITLE_COLOR', 'white')
    SUBTITLE_BACKGROUND = os.getenv('SUBTITLE_BACKGROUND', 'black')
    
    # Script Generation
    MIN_SCRIPT_LENGTH = 100  # characters
    MAX_SCRIPT_LENGTH = 5000  # characters
    DEFAULT_SCRIPT_LANGUAGE = 'en'
    
    # Effects Configuration
    AVAILABLE_EFFECTS = [
        'fade',
        'blur',
        'brightness',
        'contrast',
        'sepia',
        'grayscale',
        'zoom',
        'pan',
    ]
    
    AVAILABLE_TRANSITIONS = [
        'fade',
        'wipe',
        'dissolve',
        'slide',
        'push',
        'cover',
    ]
    
    # Music Configuration
    MUSIC_FOLDER = './assets/music'
    SOUND_EFFECTS_FOLDER = './assets/sounds'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/app.log')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig