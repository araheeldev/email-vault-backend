from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text
from extensions import db 
from rococo.models import VersionedModel
from datetime import datetime

class User(VersionedModel, db.Model):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True) 
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    company_name = Column(String(100), nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    referral_code = Column(String(10), unique=True, nullable=True)
    referrer_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    recovery_token = Column(String(36), nullable=True)
    recovery_token_expiration = Column(DateTime, nullable=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32), nullable=True)
    card_name = Column(String(100), nullable=True) 
    billing_address = Column(String(255), nullable=True) 
    card_last_four = Column(String(4), nullable=True) 
    expiration_date = Column(String(5), nullable=True) 
   
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        self.log_action("create")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        self.log_action("update")

    def log_action(self, action):
        audit = UserAudit(
            user_id=self.id,
            action=action,
            action_time=datetime.utcnow(),
            details=f"Action '{action}' performed on user with ID {self.id}"
        )
        db.session.add(audit)
        db.session.commit()


class UserAudit(db.Model):
    __tablename__ = 'user_audit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    action = Column(String(50), nullable=False)
    action_time = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)

