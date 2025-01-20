from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# Тесты на работу реги и crud чтобы не тестить вручную


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_register_success(self):
        response = self.client.post(
            self.url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "User created", "user_id": 1})

    def test_register_missing_fields(self):
        response = self.client.post(self.url, {"username": "testuser"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"error": "Username and password are required"}
        )

    def test_register_duplicate_username(self):
        User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(
            self.url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Username already exists"})


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("login")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_success(self):
        response = self.client.post(
            self.url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logged in"})

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid credentials"})


class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("logout")

    def test_logout_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logged out"})


class UserCrudViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("user_crud")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_get_all_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"username": "testuser", "email": ""}])

    def test_create_user(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpassword",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "User created"})

    def test_update_user(self):
        response = self.client.put(
            f"{self.url}{self.user.id}/",
            {"username": "updateduser", "email": "updated@example.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User updated"})

    def test_delete_user(self):
        response = self.client.delete(f"{self.url}{self.user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User deleted"})
