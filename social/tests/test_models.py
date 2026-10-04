# tests/test_models.py
from django.contrib.auth import get_user_model
import pytest
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
        """Test basic profile creation"""
        profile = Profile.objects.create(
            user=user,
            bio="a graphics designer"
        )

        assert profile.user ==  user
        assert profile.bio == "a graphics designer"
    

class TestPostModel:
    """Unit tests for Post model"""
    
    def test_post_creation(self, user):

        """Test post creation"""
        post = Post.objects.create(
                    user=user,
                    content="i have a Phone"
                )
        
        assert post.user == user
        assert post.content == "i have a Phone"

class TestFollowModel:

    """Unit tests for Follow model"""
    def test_follow_users(self, user):
        """Test if User A follow User B"""

        friends = Follow.objects.create(
            follower=user,
            following=user
        )

        assert friends.follower == friends.following
