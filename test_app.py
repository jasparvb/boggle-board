from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    def test_boggle_start(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('high-score'))
            self.assertIsNone(session.get('games-played'))
            self.assertIn('<h1>Boggle Board</h1>', html)
   
    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["S", "O", "C", "K", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"]]
            resp = client.get('/check-word?word=SOCK')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')

    def test_check_not_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["S", "O", "C", "K", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"]]
            resp = client.get('/check-word?word=asdasfdsf')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')

    def test_check_word_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["S", "O", "C", "K", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"],["A", "B", "C", "D", "E"]]
            resp = client.get('/check-word?word=SHOE')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')
    
    def test_post_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high-score'] = 2
            resp = client.post('/post-score', json={'score': 6})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['high-score'], 6)
