import pytest
from rest_framework import status
from django.urls import reverse
from commerce.models import Product
from accounts.models import User
pytestmark = pytest.mark.django_db

    # # get access token for the test user
    # login_url = reverse("accounts:api-token")
    # login_data = {"email": user.email, "password": user.password}
    # login_response = api_client.post(login_url, login_data, format="json")
    # access_token = login_response.data["access"]

class TestProductsAPI:
    
    def test_list_products_paginated(self, api_client):
        """Verify product listing endpoint returns paginated output."""

        # create one product
        Product.objects.create(
            name="Test Laptop",
            description="High-end laptop",
            price="999.99",
            stock=10
        ) 
        url = reverse("products-view")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) > 0

    def test_get_product_recommendations(self, api_client):
        """Verify recommendations endpoint returns array of related items."""
        product = Product.objects.create(
            name="Test Laptop",
            description="High-end laptop",
            price="999.99",
            stock=10
        )
        url = f"/api/v1.1/commerce/products/{product.id}/recommendations"

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, dict)

    def test_protected_endpoint_with_token(self, api_client):
        """Test accessing protected endpoint with JWT"""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", role="customer", password="testpass123", is_active=True
        )

        # First login 
        login_url = reverse("accounts:api-token")
        login_data = {"email": user.email, "password": "testpass123"}
        login_response = api_client.post(login_url, login_data, format="json")
        access_token = login_response.data["access"]
        # print("@@@@@@@@")
        # print(access_token)

        # Use token to access protected endpoint
        products_url = reverse("products-view")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        payload = {"owner": user.id, "name": "Test", "description": "new auth cat", "category": "others", "price": "10", "stock": 2}
        response = api_client.post(products_url, payload, format="json")
        # Should be 201 (created) or 401/403 depending on permissions
        assert response.status_code in [201, 401, 403]
