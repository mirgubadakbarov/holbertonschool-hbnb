import unittest
from app.services.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        UserService.users = []

    def test_create_user(self):
        user = UserService.create_user("test@example.com", "password", "First", "Last")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(len(UserService.users), 1)

    def test_create_duplicate_user(self):
        UserService.create_user("test@example.com", "password", "First", "Last")
        with self.assertRaises(ValueError):
            UserService.create_user("test@example.com", "password", "First", "Last")

if __name__ == '__main__':
    unittest.main()
