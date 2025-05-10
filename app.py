"""
Монолитное Flask-приложение для деплоя на Render
"""
import os
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, Blueprint, jsonify, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Инициализация Flask и расширений
app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Загрузка конфигурации
app_settings = os.getenv('APP_SETTINGS', 'development')

# Базовый каталог проекта
BASE_DIR = Path(__file__).resolve().parent

# Настройка конфигурации
if app_settings == 'production':
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'prod-secret-key')
    app.config['DEBUG'] = False
    
    # PostgreSQL для продакшена
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or f'sqlite:///{BASE_DIR / "prod.db"}'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
else:
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR / "dev.db"}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db = SQLAlchemy(app)

# Модели базы данных
class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Устанавливает хеш пароля"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Проверяет пароль"""
        return check_password_hash(self.password_hash, password)

# Создаем таблицы при первом запуске
with app.app_context():
    db.create_all()

# Маршруты
@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', title='Главная страница')

@app.route('/about')
def about():
    """Страница о нас"""
    return render_template('about.html', title='О нас')

@app.route('/api/status')
def api_status():
    """API-эндпоинт для проверки статуса"""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Эндпоинт проверки работоспособности для Render"""
    return jsonify({'status': 'ok'})

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 