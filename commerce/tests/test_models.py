# tests/test_models.py
from django.contrib.auth import get_user_model
import pytest
from commerce.models import Product, Order, OrderItem

User = get_user_model()

# Applies DB access across this file
pytestmark = pytest.mark.django_db  

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        is_active=True
    )

class TestProductModel:
    """Unit tests for Product model"""
    
    def test_product_creation(self, user):
        """Test basic product creation"""
        product = Product.objects.create(
            owner=user,
            name='Laptop',
            price=39.92,
            stock=5
        )

        assert str(product) ==  "Laptop"
        assert float(product.price) == 39.92
    
    def test_product_stock_status(self, user):
        """Test stock-related properties"""
        product = Product.objects.create(
            owner=user,
            name='Phone',
            price=34.99,
            stock=3
        )
        
        # out of stock
        assert product.stock >= 1 


class TestOrderModel:
    """Unit tests for Order model"""
    
    def test_order_total_calculation(self, user):

        """Test order total amount calculation"""
        product = Product.objects.create(
                    owner=user,
                    name='Phone',
                    price=34.99,
                    stock=3
                )
        
        order = Order.objects.create(user=user, order_status='pending')
        OrderItem.objects.create(
            order=order,
            product=product,
            price=100,
            quantity=2
        )
        assert order.total_amount() == 200

class TestOrderItemModel:

    """Unit tests for OrderItem model"""
    def test_order_item_total_price(self, user):
        """Test total price calculation for order item"""

        product = Product.objects.create(
            owner=user, name='Headphones', price=50, stock=10
        )
        order = Order.objects.create(user=user, order_status='pending')
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            price=50,
            quantity=3
        )

        assert order_item.total_price() == 150

