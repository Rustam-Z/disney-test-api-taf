from typing import List, Optionalfrom pydantic import BaseModel, StrictInt, constr, StrictStrfrom api.responses.response_models import SuccessResponseclass _FacilityField(BaseModel):    id: StrictInt    name: constr(min_length=1, strict=True)class _Metro(BaseModel):    id: StrictInt    facility: StrictInt    human_readable: constr(min_length=1, strict=True)    qr_code: constr(min_length=1, strict=True)    rfid_tag_id: constr(min_length=1, strict=True)    laundry_status: constr(min_length=1, strict=True)    process_status: constr(min_length=1, strict=True)class _MetroWithFacility(_Metro):    facility: _FacilityField    status: constr(min_length=1, strict=True)  # TODO: use selection"""Get metro"""class GetMetroSuccessResponse(SuccessResponse):    data: _MetroWithFacility"""Get all metros"""class _GetAllMetrosDataField(BaseModel):    count: StrictInt    next: Optional[StrictStr]    previous: Optional[StrictStr]    results: _MetroWithFacilityclass GetAllMetrosSuccessResponse(SuccessResponse):    data: _GetAllMetrosDataField"""Create metro"""class CreateMetroSuccessResponse(SuccessResponse):    data: _Metro"""Update metro"""class UpdateMetroSuccessResponse(SuccessResponse):    data: _Metro