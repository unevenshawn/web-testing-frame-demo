import unittest

import pytest


@pytest.fixture(scope="session", autouse=True)
def gob():
    print("\n******************************************************************************")


# @pytest.mark.usefixtures("gob")
def test_outofunitclass(gob, cache):
    print("test_outofunitclass")
    print(type(cache))
    cache.set("to test if is cache", "all on my way ")
    # print(cache.get("to test if is cache"))


# @pytest.mark.usefixtures("gob")
def test_outofunitclass2(gob, cache):
    print("test_outofunitclass")
    print(cache.get("to test if is cache", None))


def test_3(gob):
    print("this is test_3")

# # python -m unittest discover -s testcase
# class test_Uni(unittest.TestCase):
#     def test_g(self, gob, cache):
#         cache.set("to test if is cache", "all on my way ")
#         print("this is a")
#
#     def test_c(self, gob, cache):
#         print(cache.get("to test if is cache"))
#         print("this is b")
