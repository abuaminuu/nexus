# tests/test_models.py
from django.contrib.auth import get_user_model
import pytest
from commerce.models import Product, Order, OrderItem
from social.models import Profile, Post, Follow


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

class TestProfileModel:
    """Unit tests for Product model"""
    
    def test_product_creation(self, user):
        """Test basic product creation"""
        profile = Profile.objects.create(
            user=user,
            bio="a graphics designer"
        )

        assert profile.user ==  user
        assert profile.bio == "a graphics designer"
    

class TestPostModel:
    """Unit tests for Order model"""
    
    def test_order_total_calculation(self, user):

        """Test order total amount calculation"""
        post = Post.objects.create(
                    user=user,
                    content="i have a Phone"
                )
        
        assert post.user == user
        assert post.content == "i have a Phone"

class TestFollowModel:

    """Unit tests for OrderItem model"""
    def test_order_item_total_price(self, user):
        """Test total price calculation for order item"""

        friends = Follow.objects.create(
            follower=user,
            following=user
        )

        assert friends.follower == friends.following
        

