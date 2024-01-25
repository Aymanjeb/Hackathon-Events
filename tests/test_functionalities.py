import unittest
from app import app, mongo  
from unittest.mock import patch

class FlaskTestCase(unittest.TestCase):
    def test_index_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    @patch('pymongo.collection.Collection.find_one')
    def test_correct_login(self, mock_find):
        mock_find.return_value = {
            'username': 'testuser',
            'password': '123',
            'email': 'test@example.com'
        }
        with app.test_client() as client:
            response = client.post('/login', data={
                'username': 'testuser',
                'password': '123'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            with client.session_transaction() as sess:
                self.assertEqual(sess['username'], 'testuser')
            self.assertIn(b'Mes r\xc3\xa9servations', response.data) 
            self.assertIn(b'D\xc3\xa9connexion', response.data)

if __name__ == '__main__':
    unittest.main()
