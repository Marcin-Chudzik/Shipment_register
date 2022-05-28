from datetime import datetime

from shipment_register import actual_date


def test_actual_date():
    assert actual_date() == datetime.now().strftime("%d-%m-%Y")
