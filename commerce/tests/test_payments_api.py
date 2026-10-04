import pytest
from unittest.mock import patch
from rest_framework import status
from accounts.models import User
from commerce.models import Order

@pytest.mark.django_db
class TestPaymentWebhooksAndCallbacks:

    def test_payment_callback_verifies_and_marks_order_paid(self, api_client):
        """Test payment gateway redirect callback updates order status to 'paid'."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", role="customer", password="testpass123", is_active=True
        )

        order = Order.objects.create(user_id=user.id, order_status="pending", amount=5000, tx_ref="TX12345")
        url = f"/api/v1.1/commerce/payments/callback/{order.id}?status=successful&tx_ref=TX12345"
        
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # refresh the order from the database to check updated status
        order.refresh_from_db()
        assert order.tx_ref == "TX12345"
        # for testing only, but its webhook that actually update order instance
        # callback gives hope to a user
        assert response.data.get("order_status") == "paid"
