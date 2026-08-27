from flask import Flask

from config import Config
from app.extensions import db, migrate, bcrypt, login_manager
from app.models import Usuario


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from app.routes import main
    from app.auth.routes import auth
    from app.lotes.routes import lotes

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(lotes)

    return app