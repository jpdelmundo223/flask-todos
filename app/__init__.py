from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "thisisaverysecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .auth import auth
    app.register_blueprint(auth)

    from .todo import todo
    app.register_blueprint(todo)

    from .models import Users, Todos
    db.create_all(app=app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/page_not_found.html'), 404

    return app