import random

import pytest

import data
from api.endpoints.order.driver_assignment_api import DriverAssignmentAPI
from api.enums.params import Param


@pytest.fixture()
def driver_assignment(
    create_fake_facility,
    create_fake_role,
    create_fake_user,
    create_fake_truck_superuser,
    create_fake_order_superuser,
):
    # Create facility
    facility_payload, facility_response, facility_model = create_fake_facility(no_of_customers=2)
    facility_id = facility_model.data.id
    customer_id = random.choice(facility_model.data.customers)

    # Create driver role
    role_payload, role_response, role_model = create_fake_role(is_driver=True, facility_id=facility_id)
    driver_role_id = role_model.data.id
    assert role_model.data.facility == facility_id

    # Create driver
    driver_payload, driver_response, driver_model = create_fake_user(facility_id=facility_id, role_id=driver_role_id)
    driver_id = driver_model.data.id
    assert driver_model.data.facility == facility_id

    # Create truck
    truck_payload, truck_response, truck_model = create_fake_truck_superuser(facility_id=facility_id)
    truck_id = truck_model.data.id
    assert truck_model.data.facility == facility_id

    # Create orders
    order_payload, order_response, order_model = create_fake_order_superuser(
        facility_id=facility_id,
        customer_id=customer_id
    )
    dropoff_date_start = order_model.data.dropoff_date_start
    order_id = order_model.data.id
    assert order_model.data.facility == facility_id
    assert order_model.data.customer == customer_id

    return {
        'facility_id': facility_id,
        'customer_id': customer_id,
        'driver_id': driver_id,
        'truck_id': truck_id,
        'order_id': order_id,
        'dropoff_date_start': dropoff_date_start
    }


@pytest.fixture()
def assign_orders_to_truck_and_drivers(client, driver_assignment, request):
    setup = request.getfixturevalue('driver_assignment')
    facility_id = setup.get('facility_id')
    truck_id = setup.get('truck_id')
    driver_id = setup.get('driver_id')
    order_id = setup.get('order_id')
    dropoff_date_start = setup.get('dropoff_date_start')

    # Assign orders to drivers and trucks
    payload = data.fake.model.driver_assignment_to_one_order(
        truck=truck_id,
        drivers=[driver_id],
        assigned_orders=[order_id],
        unassigned_orders=[],
    )
    params = {
        Param.DATE_START_TIME_UTC.value: dropoff_date_start,
        Param.FACILITY.value: facility_id
    }
    DriverAssignmentAPI(client).assign_orders_to_truck_and_drivers(params=params, data=payload)

    return setup
