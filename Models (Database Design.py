# Using SQLAlchemy (for Flask) or Django's ORM
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class SMTPSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    smtp_server = db.Column(db.String(150), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)
    smtp_username = db.Column(db.String(150), nullable=False)
    smtp_password = db.Column(db.String(150), nullable=False)  # Should be encrypted
    encryption = db.Column(db.String(50), nullable=False)  # SSL/TLS/None
    user = db.relationship('User', backref='smtp_settings')


class SentEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())
    user = db.relationship('User', backref='sent_emails')
