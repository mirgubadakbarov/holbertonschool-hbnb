import unittest
import os
import json
from app.persistence.data_manager import DataManager
from app.models.user import User

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_storage.json'
        self.data_manager = DataManager(storage_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_get_user(self):
        user = User(email="test@example.com", password="password", first_name="First", last_name="Last")
        self.data_manager.save(user)
        retrieved_user = self.data_manager.get(user.id, "User")
        self.assertEqual(retrieved_user['email'], "test@example.com")

    def test_update_user(self):
        user = User(email="test@example.com", password="password", first_name="First", last_name="Last")
        self.data_manager.save(user)
        user.first_name = "Updated"
        self.data_manager.update(user)
        retrieved_user = self.data_manager.get(user.id, "User")
        self.assertEqual(retrieved_user['first_name'], "Updated")

    def test_delete_user(self):
        user = User(email="test@example.com", password="password", first_name="First", last_name="Last")
        self.data_manager.save(user)
        self.data_manager.delete(user.id, "User")
        retrieved_user = self.data_manager.get(user.id, "User")
        self.assertIsNone(retrieved_user)

if __name__ == '__main__':
    unittest.main()
