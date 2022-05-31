from datetime import datetime
from sqlite3 import Error

from shipment_register import actual_date, Database


def test_actual_date():
    test_func = actual_date
    assert test_func() == datetime.now().strftime("%d-%m-%Y")


def test_valid_insert_statement(database_instance, valid_shipment_statement: str):
    assert Database.insert_statement(database_instance, valid_shipment_statement) is None


def test_invalid_insert_statement(database_instance, invalid_shipment_statement: str):
    assert Database.insert_statement(database_instance, invalid_shipment_statement) == Error


