# tests/test_auth.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from commerce.models import User


class AuthenticationTest(APITestCase):
    """Critical authentication tests"""
    
    def setUp(self):
        self.valid_user = User.objects.create_user(
            username="testuser", email="test@test.com", role="customer", password="testpass123", is_active=True
        )
        self.invalid_user = User.objects.create_user(
            username="invaliduser", email="invalid_email@test.com", role="invalid_customer", password="invalidpass123"
        )

    def test_user_registration(self):
        """Test user can register"""
        url = reverse("accounts:signup-view")
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "role": "customer",
            "password": "password123"
        }
        # data = json.loads(data)
        response = self.client.post(url, data)
        # makig sure user is redirected to landing page after succesful registration
        self.assertRedirects(response, reverse("accounts:landing-page"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
   
    def test_user_login(self):
        """Test user can login and get tokens"""
        url = reverse("accounts:login-view")
        data = {
            "username": self.valid_user.email,
            "password": "testpass123"
        }

        response = self.client.post(url, data)
        # checks that user is redirected to landing page after succesful login 
        self.assertRedirects(response, reverse("accounts:landing-page"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_get_tokens(self):
        """Test user can login and get tokens"""
        url = reverse("accounts:api-token")
        data = {
            "email": self.valid_user.email,
            "password": "testpass123"
        }

        response = self.client.post(url, data, format="json")
        print("SimpleJWT Error:", response.data)  # This will print {"detail": "No active account found with the given credentials"} or similar
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # checks that access token is available and can be refreshed
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_refresh_token(self):
        """Test refresh token generates a new access token."""
        # Obtain initial tokens
        # 1. Obtain initial tokens (using "email" key)
        api_token_url = reverse("accounts:api-token")
        login_response = self.client.post(
            api_token_url,
            {"email": self.valid_user.email, "password": "testpass123"},
            format="json"
        )

        # Catch initial failure before accessing dictionary keys
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
    
        refresh_token = login_response.data["refresh"]

        # 2. Request a new access token using the refresh view
        refresh_url = reverse("accounts:token-refresh")
        response = self.client.post(
            refresh_url,
            {"refresh": refresh_token},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

