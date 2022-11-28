import pymongo as pm

import pytest

import db_connect as dbc

TEST_DB = dbc.GROC_DB
TEST_COLLECT = 'test_collect'
TEST_NAME = 'test'


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})


@pytest.mark.skip("Can't run this test untill the we figure out MongoDB Connection.")
def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None


@pytest.mark.skip("Can't run this test untill the we figure out MongoDB Connection.")
def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'invalid field in db'})
    assert ret is None
