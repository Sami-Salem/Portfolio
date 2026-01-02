import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    
    # API Keys (loaded from environment)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SERP_API_KEY = os.getenv('SERP_API_KEY')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    @staticmethod
    def validate_config():
        """Validate required configuration"""
        required = []
        if not Config.SECRET_KEY or Config.SECRET_KEY == 'dev-secret-key-change-in-production':
            required.append('SECRET_KEY')
        
        if required:
            raise ValueError(f"Missing required configuration: {', '.join(required)}")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    RATE_LIMIT_PER_MINUTE = 30  # Stricter in production

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    RATE_LIMIT_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}