import random
from flask import session
from flask_mail import Message
from app import mail

def send_verification_code(email):
    code = str(random.randint(100000, 999999))
    session['email_verification_code'] = code
    session['email_verification_target'] = email

    msg = Message("Your GameNalyzer Verification Code",
                  recipients=[email])
    msg.body = f"Your verification code is: {code}\n\nIf you did not request this, please ignore."
    mail.send(msg)
