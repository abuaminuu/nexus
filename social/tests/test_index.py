import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

class TestIndexView:

    def test_index_view(self, api_client):
        url = reverse("index")

        response = api_client.get(url)

        # index is reachable
        assert response.status_code == 200
        # index returned page object
        assert "page_object" in response.context



