import random

import pytest

import data
from api.endpoints.customer.customer_api import CustomerAPI
from api.endpoints.driver_process.driver_process_api import DriverProcessAPI
from api.endpoints.staging.staging_api import StagingAPI


@pytest.fixture()
def assign_metro(
    client,
    create_fake_facility,
    create_fake_order_superuser,
    create_fake_cart_superuser,
):
    def _fixture(**kwargs):
        if 'facility_id' not in kwargs:
            facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=1)
            kwargs['facility_id'] = facility_model.data.id
            kwargs['customer_id'] = random.choice(facility_model.data.customers)

        facility_id = kwargs['facility_id']
        customer_id = kwargs['customer_id']

        # Create order
        order_payload, order_response, order_model = create_fake_order_superuser(
            facility_id=facility_id,
            customer_id=customer_id
        )
        order_id = order_model.data.id
        assert order_model.data.facility == facility_id
        assert order_model.data.customer == customer_id;

        # Create cart
        cart_payload, cart_response, cart_model = create_fake_cart_superuser(
            facility_id=facility_id
        )
        cart_id = cart_model.data.id
        metro_id = cart_model.data.metro.id
        metro_qr_code = cart_model.data.metro.qr_code
        metro_config_qr_code = cart_model.data.metro_config.qr_code

        # Assign metro to order
        payload = {
            "metro_qr_code": metro_qr_code,
            "order_id": order_id
        }
        StagingAPI(client).assign_metro(payload)

        return {
            'facility_id': facility_id,
            'customer_id': customer_id,
            'order_id': order_id,
            'cart_id': cart_id,
            'metro_id': metro_id,
            'metro_qr_code': metro_qr_code,
            'metro_config_qr_code': metro_config_qr_code,
            'dropoff_date_start': order_model.data.dropoff_date_start
        }

    yield _fixture


@pytest.fixture()
def staging(client, request):
    setup = request.getfixturevalue('assign_metro')()
    customer_id = setup.get('customer_id')
    order_id = setup.get('order_id')

    # Submit action
    customer_response, customer_model = CustomerAPI(client).get_customer(customer_id)
    customer_barcode = customer_model.data.barcode
    payload = {
        "order_id": order_id,
        "disney_order_id": data.fake.pyint(),
        "customer_barcode": customer_barcode
    }
    StagingAPI(client).submit_action(payload)

    return setup


@pytest.fixture()
def deliver_order(client, request):
    setup = request.getfixturevalue('staging')
    order_id = setup.get('order_id')
    metro_qr_code = setup.get('metro_qr_code')

    # Reader metro scan.
    payload = {
        "reader_name": f"Reader: {data.fake.ean13()}",
        "mac_address": f"192.168.0.{random.randint(0, 255)}",
        "tag_reads": [
            {
                "antennaPort": random.randint(1, 9),
                "epc": metro_qr_code
            }
        ]
    }
    DriverProcessAPI(client).reader_metro_scan(payload)

    # Driver metro scan.
    payload = {
        "order_id": order_id,
        "qr_code": metro_qr_code
    }
    DriverProcessAPI(client).driver_metro_scan(payload)

    payload = {
        "order_id": order_id
    }

    # Act
    response, model = DriverProcessAPI(client).submit(payload)

    setup.update({
        'response': response,
        'model': model,
    })

    return setup

