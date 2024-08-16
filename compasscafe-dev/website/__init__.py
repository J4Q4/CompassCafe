from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import datetime
import atexit
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
DB_NAME = "database.db"


mail = Mail()
scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "XZ.x_+hiZZs!y9T"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'compasscafesmc.wacky.dev'
    app.config['MAIL_PORT'] = '465'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'noreply@compasscafesmc.wacky.dev'
    app.config['MAIL_PASSWORD'] = 'WAKABAKA@123'
    app.config['TESTING'] = False

    # https://wacky.dev:2096/cpsess2619298596/3rdparty/roundcube/?_task=mail&_mbox=INBOX
    # Temporary Mass Email Configuration

    db.init_app(app)
    mail.init_app(app)

    from .views import views, notifyDuty
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

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

    # @app.route('/send-email')
    # def test_email():
    #     user_email = "18065@my.sanctamaria.school.nz"
    #     notifyEmail(user_email, 'Week B', 'Thursday')
    #     return "Email sent to " + user_email

    from .models import User

    # Ensure Notifications are Working (With Context)
    def notifyDuty_context():
        with app.app_context():
            notifyDuty()

    # Schedule Barista Notifications for Day
    scheduler.add_job(notifyDuty_context, 'cron', hour=8, minute=30)  #8:30 AM

    scheduler.start()

    # Scheduler Off on App Exit
    atexit.register(lambda: scheduler.shutdown(wait=False))

    return app


# EMAIL FUNCTIONS


# NEW REGISTERED USERS

def welcomeEmail(user_email):
    try:
        msg = Message("Welcome to Compass Cafe Website!",
                      sender="noreply@compasscafesmc.wacky.dev",
                      recipients=[user_email])
        msg.body = "Hello user! We’re glad to have you aboard."
        mail.send(msg)
        return "Sent"
    except Exception as errorEmail:
        print(f"Failed to send email to {user_email}: {errorEmail}")
        return "Failed"


# ACCEPTED APPLICANTS

def baristaEmail(user_email, week, day):
    try:
        msg = Message("Welcome to the Team! - Compass Cafe",
                      sender="noreply@compasscafesmc.wacky.dev",
                      recipients=[user_email])
        # Include week and day in the email body
        msg.body = f"Hello! You've been selected to be part of the barista team at Sancta Maria College on {day} of {week}. Looking forward to seeing you! :)"
        mail.send(msg)
        return "Sent"
    except Exception as errorEmail:
        print(f"Failed to send email to {user_email}: {errorEmail}")
        return "Failed"


# NOTIFY ON DUTY

def notifyEmail(user_email, week, day):
    try:
        msg = Message("You're on duty today! - Compass Cafe",
                      sender="noreply@compasscafesmc.wacky.dev",
                      recipients=[user_email])
        msg.body = f"Hello! You're on duty today, {day} of {week}. If there has been an error, please contact your supervisor."
        # SHOW BUTTON FOR VIEWING SCHEDULE ON THE WEBSITE TO SHOW PROOF.
        mail.send(msg)
        return "Sent"
    except Exception as errorEmail:
        print(f"Failed to send email to {user_email}: {errorEmail}")
        return "Failed"
