from flask import Flask
from config import db, migrate, bcrypt, jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

# import routes AFTER app creation (important fix)
from flask import request, jsonify
from models import User, Note
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# AUTH ROUTES (unchanged)
@app.post('/signup')
def signup():
    data = request.get_json()

    user = User(username=data.get('username'))
    user.password_hash = data.get('password')

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))

    return {
        "token": token,
        "user": {"id": user.id, "username": user.username}
    }, 201


@app.post('/login')
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.authenticate(data.get('password')):
        token = create_access_token(identity=str(user.id))

        return {
            "token": token,
            "user": {"id": user.id, "username": user.username}
        }, 200

    return {"errors": ["Invalid credentials"]}, 401


@app.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    return {"id": user.id, "username": user.username}


@app.route('/')
def home():
    return {"message": "API running"}