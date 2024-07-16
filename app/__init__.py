from flask import Flask, render_template, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from flask_scss import Scss
from flask_login import current_user

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    scss = Scss(app, static_dir='app/static', asset_dir='app/static/sass', load_paths=['app/static/sass'])    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.monitor import monitor_bp
    app.register_blueprint(monitor_bp, url_prefix='/monitor')

    from app.settings import settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    from .models import User

    with app.app_context():
        db.create_all()

    @login.user_loader  # Define user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    #@app.before_request
    #def check_login():
        #if current_user.is_authenticated:
            #return redirect(url_for('monitor.index'))

    
    
    return app