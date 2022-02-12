import pytest


@pytest.fixture(scope='function', autouse=False)
def suit_fixture():
    print("config environment")