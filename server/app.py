from flask import Flask
from config import db, migrate, bcrypt, jwt
from models import User, Note

app = Flask(__name__)

# basic config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # change later if needed

# init extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

# simple route (just to test)
@app.route('/')
def home():
    return {"message": "API is running"}