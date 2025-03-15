from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import datetime
from markupsafe import Markup

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # 注册自定义过滤器
    @app.template_filter('strftime')
    def _jinja2_filter_strftime(date_format, timestamp=None):
        if timestamp is None:
            return datetime.datetime.now().strftime(date_format)
        return timestamp.strftime(date_format)
    
    @app.template_filter('nl2br')
    def _jinja2_filter_nl2br(s):
        if s is None:
            return ""
        return Markup(s.replace('\n', '<br>'))
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.album import bp as album_bp
    app.register_blueprint(album_bp, url_prefix='/album')
    
    from app.timeline import bp as timeline_bp
    app.register_blueprint(timeline_bp, url_prefix='/timeline')
    
    from app.calendar import bp as calendar_bp
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    
    return app

from app import models 