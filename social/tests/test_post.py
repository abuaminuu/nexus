import pytest
from django.urls import reverse
from accounts.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def user():
    return User.objects.create(
        username= "newuser",
        email= "newuser@test.com",
        role="customer",
        password="password123"
    )


class TestPostView:

    def test_post_view(self, api_client):
        url = reverse("post")
        
        payload = { "user":user, "contents":"post from test!" }
        
        response = api_client.post(url, payload=payload)
        # print("@@@@@")
        # print(response.headers)

        # post returned redirect to correct route
        assert response.status_code == 302
        # social route returned
        assert response["Location"]  == "/social/"

