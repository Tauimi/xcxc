"""
Инициализация Flask-приложения
"""
import os
from flask import Flask

def create_app():
    """Создает экземпляр приложения Flask."""
    # Создаем экземпляр приложения Flask
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Загружаем конфигурацию
    app_settings = os.getenv('APP_SETTINGS', 'development')
    app.config.from_object(f'app.config.{app_settings.capitalize()}Config')
    
    # Регистрируем маршруты
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Инициализируем базу данных
    from app.models.db import db
    db.init_app(app)
    
    # Создаем таблицы при первом запуске
    with app.app_context():
        db.create_all()
        
    # Эндпоинт проверки работоспособности для Render
    @app.route('/health')
    def health():
        return {'status': 'ok'}
    
    return app 