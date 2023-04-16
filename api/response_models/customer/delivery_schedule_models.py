from typing import List, Optional

from pydantic import BaseModel, StrictInt, constr, StrictStr

from api.response_models.response_models import SuccessResponse


class _DeliverySchedule(BaseModel):
    id: StrictInt
    facility: StrictInt
    customer: StrictInt
    days: List[constr(min_length=1, strict=True)]
    start_time: constr(min_length=1, strict=True)
    end_time: constr(min_length=1, strict=True)


class _FacilityField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _CustomerField(BaseModel):
    id: StrictInt
    name: constr(min_length=1, strict=True)


class _DeliveryScheduleComplex(_DeliverySchedule):
    facility: _FacilityField
    customer: _CustomerField


"""
Get delivery schedule
"""


class GetDeliveryScheduleSuccessResponse(SuccessResponse):
    data: _DeliveryScheduleComplex


"""
Get all delivery schedules
"""


class _GetAllDeliveryScheduleDataField(BaseModel):
    count: StrictInt
    next: Optional[StrictStr]
    previous: Optional[StrictStr]
    results: List[_DeliveryScheduleComplex]


class GetAllDeliveryScheduleSuccessResponse(SuccessResponse):
    data: _GetAllDeliveryScheduleDataField


"""
Create delivery schedule
"""


class CreateDeliveryScheduleSuccessResponse(SuccessResponse):
    data: _DeliverySchedule
