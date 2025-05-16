import unittest
from app import create_app, db
from app.models import User
from flask import session
from werkzeug.security import generate_password_hash
from app.config import TestingConfig

class AuthTestCase(unittest.TestCase):
    def setUp(self):
          
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register(self):
        with self.client.session_transaction() as sess:
            sess['email_verification_code'] = '123456'
            sess['email_verification_target'] = 'test@gmail.com'

        response = self.client.post('/register', data={
        'username': 'tester',
        'email': 'test@gmail.com',
        'verification_code': '123456',  
        'password': 'Test123!',
        'confirm_password': 'Test123!',
        'submit': 'Register' 
    }, follow_redirects=True)

        self.assertNotIn(b'Register', response.data)
        self.assertTrue(b'Login' in response.data or b'Welcome' in response.data)
        user = User.query.filter_by(username='tester').first()
        self.assertIsNotNone(user)

    def test_login_logout(self):
        hashed_pw = generate_password_hash('Test123!')
        user = User(username='tester', email='test@example.com', password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        
        response = self.client.post('/login', data={
            'username': 'tester',
            'password': 'Test123!'
        }, follow_redirects=True)

        self.assertIn(b'Logout', response.data)

        
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)
