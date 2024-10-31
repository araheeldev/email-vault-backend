from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_jwt_extended import create_access_token
from common.messaging.email_sender import send_verification_email, send_recovery_email
from common.models.user import User
import os
import pyotp
import datetime
from uuid import uuid4
import qrcode

def signup_user(data):
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    company_name = data.get('companyName')
    email = data.get('email')
    password = data.get('password')
    referral_code = data.get('referralCode')
    card_name = data.get('cardName')
    card_number = data.get('cardNumber')
    expiration_date = data.get('expirationDate')
    card_last_four = card_number[-4:] if card_number else None

    referrer = None
    if referral_code:
        referrer = current_app.user_repository.find_by_referral_code(referral_code)
        if not referrer:
            return {"message": "Invalid referral code"}, 400

    password_hash = generate_password_hash(password)
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        company_name=company_name,
        email=email,
        password_hash=password_hash,
        referrer_id=referrer.id if referrer else None,
        referral_code=str(uuid4())[:6], 
        card_name=card_name,
        card_last_four=card_last_four,
        expiration_date=expiration_date
    )

    current_app.user_repository.save_user(new_user)
    confirmation_link = f"{os.getenv('FRONTEND_URL')}/verify/{new_user.id}"
    send_verification_email(new_user, confirmation_link)

    return {"message": "User created successfully, verification email sent"}

def login_user(data):
    email = data.get('email')
    password = data.get('password')

    user = current_app.user_repository.find_by_email(email)
    if user and check_password_hash(user.password_hash, password):
        if user.two_factor_enabled:
            return {"message": "Two-factor authentication required", "requires_2fa": True}, 401
        else:
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
    return {"message": "Invalid credentials"}, 401

def enable_two_factor(user_id):
    user = current_app.user_repository.get_one({'id': user_id})
    if not user:
        return {"message": "User not found"}, 404

    user.two_factor_secret = pyotp.random_base32()
    current_app.user_repository.save(user)

    totp = pyotp.TOTP(user.two_factor_secret)
    qr_url = totp.provisioning_uri(name=user.email, issuer_name="EmailVaultApp")
    return {"qr_url": qr_url}

def verify_login_2fa(data):
    email = data.get('email')
    code = data.get('code')

    user = current_app.user_repository.find_by_email(email)
    if user and user.two_factor_enabled:
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(code):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
    return {"message": "Invalid 2FA code"}, 401

def verify_account(user_id):
    user = current_app.db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"message": "User not found"}, 404

    if user.is_verified:
        return {"message": "Account already verified"}, 200

    user.is_verified = True
    user.verification_date = datetime.datetime.utcnow()
    current_app.db.session.commit()

    return {"message": "Account verified successfully"}, 200

def password_recovery(data):
    email = data.get('email')
    user = current_app.user_repository.find_by_email(email)
    if not user:
        return {"message": "User not found"}, 404

    token = str(uuid4())
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    current_app.user_repository.set_recovery_token(user.id, token, expiration)

    recovery_link = f"{os.getenv('FRONTEND_URL')}/reset-password/{token}"
    send_recovery_email(user, recovery_link)

    return {"message": "Password recovery email sent"}
