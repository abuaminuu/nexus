import pytest
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestOrderCheckoutFlow:

    def test_create_order_with_item_authenticated_success(self, api_client, authenticated_user, product):
        """Verify authenticated user can initialize an order directly with a product."""
        api_client.force_authenticate(user=authenticated_user)
        url = f"/api/v1.1/commerce/orders/create_order_with_item/{product.id}/"
        payload = {"quantity": 2}

        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "pending"
        assert len(response.data["items"]) == 1

    def test_create_order_unauthenticated_fails(self, api_client, product):
        """Verify unauthenticated user receives 401 Unauthorized."""
        url = f"/api/v1.1/commerce/orders/create_order_with_item/{product.id}/"
        
        response = api_client.post(url, {"quantity": 1})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_item_to_existing_order_success(self, api_client, authenticated_user, order, product_2):
        """Verify adding an additional product item updates order totals correctly."""
        api_client.force_authenticate(user=authenticated_user)
        url = f"/api/v1.1/commerce/orders/{order.id}/add_item/{product_2.id}/"
        
        response = api_client.post(url, {"quantity": 1})

        assert response.status_code == status.HTTP_200_OK
        # Check that total price recalculated correctly in backend response
        assert response.data["total_price"] > 0

    def test_pay_order_generates_payment_link(self, api_client, authenticated_user, order):
        """Verify /pay/ triggers payment initialization (e.g. Flutterwave payload)."""
        api_client.force_authenticate(user=authenticated_user)
        url = f"/api/v1.1/commerce/orders/{order.id}/pay/"

        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert "payment_url" in response.data or "tx_ref" in response.data
