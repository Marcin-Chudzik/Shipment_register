import pytest
from shipment_register import Database

"""Tests fixtures"""


@pytest.fixture
def database_instance():
    return Database()


@pytest.fixture
def valid_shipment_statement():
    return f"INSERT INTO shipments VALUES('Title', '001', 'Article', '100', '30-05-2022')"


@pytest.fixture
def invalid_shipment_statement():
    return f"INSERT INTO shipments VALUES( '', '', '', '')"
