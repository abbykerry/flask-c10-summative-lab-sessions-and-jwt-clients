from flask import Flask, request, jsonify
from config import db, migrate, bcrypt, jwt
from models import User, Note
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

#Auth roles
@app.post('/signup')
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')

    if password != password_confirmation:
        return {"errors": ["Passwords do not match"]}, 400

    try:
        user = User(username=username)
        user.password_hash = password

        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))

        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, 201

    except Exception as e:
        return {"errors": [str(e)]}, 400


@app.post('/login')
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        token = create_access_token(identity=str(user.id))

        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, 200

    return {"errors": ["Invalid username or password"]}, 401


@app.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200


# test route
@app.route('/')
def home():
    return {"message": "API is running"}