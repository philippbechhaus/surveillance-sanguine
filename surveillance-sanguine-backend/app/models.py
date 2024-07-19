from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    tests = db.relationship('Test', backref='user', lazy=True)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    biomarkers = db.relationship('Biomarker', backref='test', lazy=True)

class Biomarker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=False)
