import os
import unittest
from unittest.mock import patch, MagicMock
from app import app, fetch_movies

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_search_status_code(self):
        response = self.app.post('/search', data=dict(movieQuery="killers of the flower moon"))
        self.assertEqual(response.status_code, 200)
        
    @patch('app.requests.get')
    def test_fetch_movies(self, mock_get):
        api_key = os.getenv('API_KEY')
        mock_movies_response = {"results":
            [{'adult': False, 'backdrop_path': '/1X7vow16X7CnCoexXh4H4F2yDJv.jpg', 'genre_ids': [80, 18, 36], 'id': 466420, 'original_language': 'en', 'original_title': 'Killers of the Flower Moon', 'overview': 'When oil is discovered in 1920s Oklahoma under Osage Nation land, the Osage people are murdered one by one—until the FBI steps in to unravel the mystery.', 'popularity': 628.26, 'poster_path': '/dB6Krk806zeqd0YNp2ngQ9zXteH.jpg', 'release_date': '2023-10-18', 'title': 'Killers of the Flower Moon', 'video': False, 'vote_average': 7.525, 'vote_count': 1892}],
              "total_pages":1,
              "total_results":1
              }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_movies_response
        mock_get.return_value = mock_response

        movies = fetch_movies("killers%20of%20the%20flower%20moon")
        mock_get.assert_called_once_with(
            f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query=killers%20of%20the%20flower%20moon"
        )
        self.assertEqual(movies, mock_movies_response['results'])

if __name__ == '__main__':
    unittest.main()