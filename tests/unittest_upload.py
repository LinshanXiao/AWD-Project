import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models import User, LeagueGame
from werkzeug.security import generate_password_hash
from io import BytesIO

class UploadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        
        hashed_pw = generate_password_hash('Test123!')
        self.test_user = User(username='tester', email='test@gmail.com', password=hashed_pw)
        db.session.add(self.test_user)
        db.session.commit()

        
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.test_user.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_csv_upload(self):
        with open('app/static/template.csv', 'rb') as f:
            data = {
                'file': (BytesIO(f.read()), 'template.csv')
            }

        response = self.client.post(
            '/upload/csv',
            data=data,
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('message', json_data)
        self.assertGreaterEqual(json_data.get('rows_added', 0), 1)

    

if __name__ == '__main__':
    unittest.main()
