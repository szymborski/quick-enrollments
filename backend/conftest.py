from django.core.cache import cache
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
