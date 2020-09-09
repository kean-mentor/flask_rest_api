import json
import os
import unittest

from app import create_app


class TestApi(unittest.TestCase):
    """Tests status codes and message/data"""

    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

    def tearDown(self):
        try:  # Not all tests create storage file
            os.remove(self.app.config['STORE_PATH'])
        except OSError:
            pass

    def test_get_all_empty(self):
        response = self.client.get('/values')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    def test_get_by_key_success(self):
        data = {'key': 'hnd145', 'value': 'Honda Civic'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/values/hnd145')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 'Honda Civic')

    def test_get_by_key_missing(self):
        response = self.client.get('/values/abc123')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Key not found!'})

    def test_get_all_prefix_success(self):
        cars = [
            {'key': 'hnd145', 'value': 'Honda Civic'},
            {'key': 'hnd371', 'value': 'Honda Accord'},
            {'key': 'tyt112', 'value': 'Toyota Celica'}
        ]
        for data in cars:
            response = self.client.post('/values', json=data)
            self.assertEqual(response.status_code, 201)

        response = self.client.get('/values?prefix=Hon')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['hnd145', 'hnd371'])

    def test_post_add(self):
        data = {'key': 'opl631', 'value': 'Opel Astra'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'Item successfully created'})

    def test_post_duplicate_key(self):
        data = {'key': 'opl631', 'value': 'Opel Astra'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 201)

        data = {'key': 'opl631', 'value': 'Opel Astra'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Item successfully updated'})

    def test_post_missing_key(self):
        data = {'value': 'Ferrari F40'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': "ERR: 'key' is a required parameter"})

    def test_post_missing_value(self):
        data = {'key': 'trk311'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': "ERR: 'value' is a required parameter"})

    def test_post_invalid(self):
        response = self.client.post('/values')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'ERR: Missing data'})

    def test_delete_existing(self):
        data = {'key': 'opl631', 'value': 'Opel Astra'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/values/opl631')
        self.assertEqual(response.status_code, 200)

        response = self.client.delete('/values/opl631')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Item successfully deleted'})

        response = self.client.get('/values/opl631')
        self.assertEqual(response.status_code, 404)

    def test_delete_missing(self):
        response = self.client.delete('/values/opl631')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Key not found!'})


if __name__ == "__main__":
    unittest.main(verbosity=2)
