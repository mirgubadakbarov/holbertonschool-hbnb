from app.models.user import User

class UserService:
    users = []

    @staticmethod
    def create_user(email, password, first_name, last_name):
        if any(user.email == email for user in UserService.users):
            raise ValueError("Email already exists")
        user = User(email, password, first_name, last_name)
        UserService.users.append(user)
        return user
