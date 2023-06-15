from .customer import create_fake_customer
from .facility import create_fake_facility
from .role import create_fake_role
from .users import (
    create_fake_user_superuser,
    create_fake_user,
)
from .category import create_fake_inventory_category
from .inventory_item_type import create_fake_inventory_item_type
from .facility_item_type import create_fake_facility_item_type_superuser
from .metro import (
    create_fake_metro_superuser,
    create_fake_metro_for_commission_superuser,
)
from .metro_item_configuration import create_fake_metro_item_configuration_superuser
from .cart_build import create_fake_cart_superuser
from .delivery_schedule import create_fake_schedule_superuser
from .order import create_fake_order_superuser
from .truck import create_fake_truck_superuser
from .inventory_location import create_fake_inventory_location_superuser
from .customer_contact import create_fake_customer_contact_superuser
from .driver_assignment import driver_assignment, assign_orders_to_truck_and_drivers
from .staging import assign_metro, staging, deliver_order
