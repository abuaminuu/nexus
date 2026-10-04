# conftest.py (at project root next to manage.py)
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Custom fixture returning DRF's APIClient for all API tests."""
    return APIClient()
