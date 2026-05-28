from fastapi import APIRouter, HTTPException, Depends
from backend.modules.location.service import LocationService
from backend.modules.location.schema import PincodeLocationResponse

router = APIRouter(prefix="/location", tags=["Location Auto-Fill"])
location_service = LocationService()

@router.get("/pincode/{pincode}", response_model=PincodeLocationResponse)
async def resolve_pincode(pincode: str):
    """
    Resolves a 6-digit Indian pincode into state, district, city, and post office.
    Validates the pincode format and proxies the request to the India Post API.
    """
    response = await location_service.fetch_pincode_details(pincode)
    if not response.success:
        # Return 400 Bad Request instead of 404 for invalid input format or not found
        raise HTTPException(status_code=400, detail=response.message)
        
    return response
