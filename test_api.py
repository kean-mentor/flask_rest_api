import unittest

from app import create_app


class TestStatusCodes(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()

    def test_get(self):
        response = self.client.get('/values')
        self.assertEqual(response.status_code, 200)

    def test_get_by_success(self):
        response = self.client.get('/values/apple')
        self.assertEqual(response.status_code, 200)

    def test_get_by_failure(self):
        response = self.client.get('/values/banana')
        self.assertEqual(response.status_code, 404)

    def test_get_prefix_success(self):
        response = self.client.get('/values?prefix=a')
        self.assertEqual(response.status_code, 200)

    def test_get_prefix_failure(self):
        response = self.client.get('/values?pre=a')
        self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        data = {'key': 'apple', 'value': 'A red, round and healty fruit.'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 201)

    def test_post_missing_key(self):
        data = {'value': 'A red, round and healty fruit.'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 400)

    def test_post_missing_value(self):
        data = {'key': 'apple'}
        response = self.client.post('/values', json=data)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
