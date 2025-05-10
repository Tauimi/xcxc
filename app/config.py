"""
Конфигурация приложения
"""
import os
from pathlib import Path

# Базовый каталог проекта
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # Настройки базы данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    # SQLite для разработки
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "dev.db"}'


class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    # Для продакшена используем PostgreSQL
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'sqlite:///{BASE_DIR / "prod.db"}'
    
    # Настройки безопасности
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    DEBUG = True
    # SQLite в памяти для тестирования
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 