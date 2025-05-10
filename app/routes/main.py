"""
Основные маршруты приложения
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models.db import db
from app.models.user import User

# Создаем Blueprint для основных маршрутов
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Главная страница"""
    # Проверяем наличие шаблона index.html
    return render_template('index.html', title='Главная страница')

@main_bp.route('/about')
def about():
    """Страница о нас"""
    # Проверяем наличие шаблона about.html
    return render_template('about.html', title='О нас')

@main_bp.route('/api/status')
def api_status():
    """API-эндпоинт для проверки статуса"""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0'
    }) 