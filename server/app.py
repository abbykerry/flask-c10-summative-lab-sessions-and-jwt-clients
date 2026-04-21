from flask import Flask
from config import db, migrate, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    # config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # import models
    from models import User, Note

    # registering blueprints
    from routes.auth import auth_bp
    from routes.notes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    @app.route('/')
    def home():
        return {"message": "API running"}

    return app


app = create_app()