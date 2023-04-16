from typing import List

from pydantic import BaseModel, StrictInt, constr

from api.response_models.response_models import SuccessResponse


class _DeliverySchedule(BaseModel):
    id: StrictInt
    facility: StrictInt
    customer: StrictInt
    days: List[constr(min_length=1, strict=True)]
    start_time: constr(min_length=1, strict=True)
    end_time: constr(min_length=1, strict=True)


"""
Get delivery schedule
"""


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _CustomerField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _GetDeliveryScheduleDataField(_DeliverySchedule):
    facility: _FacilityField
    customer: _CustomerField


class GetDeliveryScheduleSuccessResponse(SuccessResponse):
    data: _GetDeliveryScheduleDataField


"""
Create delivery schedule
"""


class CreateDeliveryScheduleSuccessResponse(SuccessResponse):
    data: _DeliverySchedule
