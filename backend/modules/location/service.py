import httpx
from typing import Optional

from backend.modules.location.schema import PincodeLocationResponse
from backend.core.config import settings

# Simple in-memory cache to reduce external API calls for duplicate pincodes
_PINCODE_CACHE = {}

class LocationService:
    """
    LocationService interfaces with the free India Post API to automatically
    resolve state, district, city, and post office from a 6-digit pincode.
    Includes simple in-memory caching for faster responses.
    """
    
    async def fetch_pincode_details(self, pincode: str) -> PincodeLocationResponse:
        # Validate 6 numeric digits
        if not pincode.isdigit() or len(pincode) != 6:
            return PincodeLocationResponse(
                success=False,
                message="Invalid Pincode: Must be exactly 6 digits."
            )
            
        # Check cache
        if pincode in _PINCODE_CACHE:
            return _PINCODE_CACHE[pincode]

        url = f"{settings.INDIA_POST_API_URL}{pincode}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and data[0].get("Status") == "Success":
                    post_offices = data[0].get("PostOffice", [])
                    if post_offices:
                        # Extract data from the first matched post office
                        po_data = post_offices[0]
                        result = PincodeLocationResponse(
                            success=True,
                            message="Pincode details fetched successfully.",
                            post_office=po_data.get("Name"),
                            city=po_data.get("Block") or po_data.get("District"), # Fallback to District if Block is empty
                            district=po_data.get("District"),
                            state=po_data.get("State"),
                            pincode=pincode
                        )
                        # Cache successful results
                        _PINCODE_CACHE[pincode] = result
                        return result
                        
                return PincodeLocationResponse(
                    success=False,
                    message="Pincode not found in India Post registry."
                )
            else:
                return PincodeLocationResponse(
                    success=False,
                    message=f"External API Error: HTTP {response.status_code}"
                )
                
        except Exception as e:
            return PincodeLocationResponse(
                success=False,
                message=f"Error connecting to India Post API: {str(e)}"
            )
