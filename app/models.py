from app import db
from werkzeug.security import check_password_hash
from sqlalchemy.sql import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    codes = db.relationship('QrCode', backref='owner', lazy='dynamic')
    
    def password_is_valid(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'User <{self.email}>'


class QrCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_value = db.Column(db.String(256))
    name = db.Column(db.String(128), nullable=True)
    embedded_value = db.Column(db.Text)
    stored_name = db.Column(db.String(64))
    updated = db.Column(db.DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'QrCode <{self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code_value': self.code_value,
            'name': self.name,
            'embedded_value': self.embedded_value,
            'stored_name': self.stored_name,
            'updated': self.updated,
            'user_id': self.user_id,
        }
    
    def update_from_dict(self, data):
        for field in ['name', 'embedded_value', 'user_id']:
            if field in data:
                setattr(self, field, data[field])
