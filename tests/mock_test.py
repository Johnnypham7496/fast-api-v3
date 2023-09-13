import unittest
from unittest import mock
from outside_api_call import rest_call_outside_api


class MockResponse(unittest.TestCase):
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    
def mock_requests_get(*args, **kwargs):
    url_index = 0

    if args[url_index] == 'https://cat-fact.herokuapp.com/facts':
        return MockResponse('[{"text": "this is a cat fact mock"}]', 200)
    
    if args[url_index] == 'https://api.chucknorris.io/jokes/random':
        return MockResponse('{"value": "this is a chuck joke}', 200)
        

class MockTest(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_tc0001_cat_chuck(self, mock_request):
        td_message = {'cat_says': 'this is a cat fact mock', 'chuck_says': 'this is a chuck joke mock'}

        response = rest_call_outside_api()

        assert response == td_message


if __name__ == '__main__':
    unittest.main()