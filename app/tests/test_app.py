import unittest
import json
from app import app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user(self):
        response = self.app.post('/users', data=json.dumps({
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        create_response = self.app.post('/users', data=json.dumps({
            'email': 'test2@example.com',
            'first_name': 'Test2',
            'last_name': 'User2'
        }), content_type='application/json')
        user_id = create_response.json['id']
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        create_response = self.app.post('/users', data=json.dumps({
            'email': 'test3@example.com',
            'first_name': 'Test3',
            'last_name': 'User3'
        }), content_type='application/json')
        user_id = create_response.json['id']
        response = self.app.put(f'/users/{user_id}', data=json.dumps({
            'first_name': 'Updated'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], 'Updated')

    def test_delete_user(self):
        create_response = self.app.post('/users', data=json.dumps({
            'email': 'test4@example.com',
            'first_name': 'Test4',
            'last_name': 'User4'
        }), content_type='application/json')
        user_id = create_response.json['id']
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()

