import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models import User, LeagueGame
from flask_login import login_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

class VisualisationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        
        hashed_pw = generate_password_hash('Test123!')
        self.user = User(username='tester', email='test@gmail.com', password=hashed_pw)
        db.session.add(self.user)
        db.session.commit()

        
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user.id)

        
        game = LeagueGame(
            user_id=self.user.id,
            game_id=9999,
            date_played=datetime.today().date(),
            game_duration="00:30:00",
            winning_team="Blue",
            league_username="tester",
            champion="Ahri",
            kills=6,
            deaths=2,
            assists=7,
            kda=6.5,
            team="Blue"
        )
        db.session.add(game)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_visualisation_page(self):
        response = self.client.get('/visualisation')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Win Rate', response.data)  
        self.assertIn(b'Ahri', response.data)       
        self.assertIn(b'Previous Game Results', response.data)

if __name__ == '__main__':
    unittest.main()
