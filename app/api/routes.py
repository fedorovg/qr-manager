import os

from app import db
from app.api import bp
from flask import request, abort, redirect, url_for, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from app.models import QrCode
from app.api.qr import generate_qr


@bp.get('/redirect/<uuid:to>')
def qr_redirect(to):
    if not (code := QrCode.query.filter_by(stored_name=str(to)).first()):
        abort(404)
    return redirect(code.embedded_value, code=302)


@bp.get('/qr_image/<int:pk>')
@jwt_required()
def get_qr_image(pk):
    if not (code := QrCode.query.filter_by(id=pk, user_id=get_jwt_identity()).first()):
        abort(404)
    path = os.path.join(current_app.config['GENERATED_CODES_PATH'], code.stored_name)
    return send_file(f'{path}.svg', mimetype='image/svg+xml')


@bp.get('/codes')
@jwt_required()
def get_codes():
    codes = QrCode.query.filter_by(user_id=get_jwt_identity()).all()
    return {
               'codes': [code.to_dict() for code in codes]
           }, 200


@bp.get('/codes/<int:pk>')
@jwt_required()
def get_code(pk):
    code = QrCode.query.filter_by(id=pk, user_id=get_jwt_identity()).first()
    if not code:
        return {'Error': 'No such QR code.'}, 404
    return code.to_dict(), 200


@bp.post('/codes')
@jwt_required()
def create_code():
    body = request.get_json()
    
    if 'embedded_value' not in body:
        return {'Error': 'QR code must have a destination value.'}, 400
    
    body['user_id'] = get_jwt_identity()  # Add or override owner id to currently logged in user
    
    code_name = str(uuid.uuid4())  # Generate a unique string
    code_value = url_for('api.qr_redirect', to=code_name, _external=True)  # Create a link
    generate_qr(code_value, code_name)
    
    code = QrCode()
    code.update_from_dict(body)
    code.code_value = code_value
    code.stored_name = code_name
    db.session.add(code)
    db.session.flush()
    code_id = code.id
    db.session.commit()
    
    return {'id': code_id}, 201


@bp.put('/codes/<int:pk>')
@jwt_required()
def update_code(pk):
    body = request.get_json()
    if not (code := QrCode.query.filter_by(id=pk, user_id=get_jwt_identity()).first()):
        return {'Error': 'QR code not found'}, 404
    
    _ = body.pop('code_value', None)  # Ignore code_value, since updating it will break existing codes.
    code.update_from_dict(body)
    db.session.commit()
    return {}, 204


@bp.delete('/codes/<int:pk>')
@jwt_required()
def delete_code(pk):
    if not (code := QrCode.query.filter_by(id=pk, user_id=get_jwt_identity()).first()):
        return {'Error': 'QR code not found'}, 404
    db.session.delete(code)
    db.session.commit()
    return {}, 204
