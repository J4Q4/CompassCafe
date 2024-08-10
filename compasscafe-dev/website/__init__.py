from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import datetime

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "XZ.x_+hiZZs!y9T"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    # 404 Page Not Found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html', user=current_user, is_404=True), 404

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Current Year
    @app.context_processor
    def currentDate():
        now = datetime.now()
        return {
            'current_year': now.year,
            'current_month': now.strftime('%B'),
            'current_day': now.strftime('%d %B %Y')
        }

    return app
