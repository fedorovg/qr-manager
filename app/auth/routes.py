from app.auth import bp
from werkzeug.security import generate_password_hash
from flask import request
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required,
    create_refresh_token,
    get_jwt_identity
)
from app import db
from app.models import User


@bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email or not password:
        return {'Error': 'To log in, you need to specify email and password.'}, 401
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'Error': 'Wrong email or password.'}, 401
    
    if not user.password_is_valid(password):
        return {'Error': 'Wrong email or password.'}, 401
    
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@bp.route('/register', methods=['POST'])
def register():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email or not password:
        return {'Error': 'To register, you need to specify email and password.'}, 401
    
    if User.query.filter_by(email=email).first():
        return {'Error': 'This email is already registered.'}, 401
    
    if len(password) < 5:
        return {'Error': 'Password is too short.'}, 401
    
    new_user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.flush()
    new_user_id = new_user.id
    db.session.commit()
    
    return {'id': new_user_id}, 201


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {}, 403
    access_token = create_access_token(identity=user)
    return {'access_token': access_token}


@bp.route('/protected')
@jwt_required()
def protected():
    """
    This exists to test Authentication
    :return:
    """
    return {
        'id': current_user.id,
        'email': current_user.email
    }
