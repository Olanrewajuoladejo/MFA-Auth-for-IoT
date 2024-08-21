import unittest
from unittest.mock import patch, call  # Import call

from app.routes import receive_data

class TestRoutes(unittest.TestCase):

    @patch('flask.request')
    def test_receive_data_success(self, mock_request):
        mock_request.json.return_value = {'temperature': 25.5, 'heartbeat': 72}
        response = receive_data()
        self.assertEqual(response, ("Data received", 200))
        mock_request.json.assert_called_once()
        self.assertEqual(mock_request.json.call_args_list, [call()])  # Use call_args_list

    @patch('flask.request')
    def test_receive_data_missing_temperature(self, mock_request):
        mock_request.json.return_value = {'heartbeat': 72}
        response = receive_data()
        self.assertEqual(response, ("Data received", 200))
        mock_request.json.assert_called_once()
        self.assertEqual(mock_request.json.call_args_list, [call()])

    @patch('flask.request')
    def test_receive_data_missing_heartbeat(self, mock_request):
        mock_request.json.return_value = {'temperature': 25.5}
        response = receive_data()
        self.assertEqual(response, ("Data received", 200))
        mock_request.json.assert_called_once()
        self.assertEqual(mock_request.json.call_args_list, [call()])

    @patch('flask.request')
    def test_receive_data_invalid_data(self, mock_request):
        mock_request.json.return_value = {'invalid_key': 'value'}
        response = receive_data()
        self.assertEqual(response, ("Data received", 200))
        mock_request.json.assert_called_once()
        self.assertEqual(mock_request.json.call_args_list, [call()])

if __name__ == '__main__':
    unittest.main()
