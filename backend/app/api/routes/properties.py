"""
Properties API routes
Property search and information
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/search")
async def search_properties(
    location: str = Query(..., description="City, State or ZIP code"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    bedrooms: Optional[int] = Query(None, ge=0),
    bathrooms: Optional[float] = Query(None, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Search for properties (mock data - integrate with Zillow/Redfin API)
    """
    # Mock property data
    properties = [
        {
            "id": 1,
            "address": "123 Main St, Austin, TX 78701",
            "price": 450000,
            "bedrooms": 3,
            "bathrooms": 2.5,
            "square_footage": 2100,
            "property_type": "single_family",
            "year_built": 2005,
            "estimated_rental_income": 2800,
            "appreciation_rate": 4.2,
            "school_rating": 8,
            "crime_rate": 25
        },
        {
            "id": 2,
            "address": "456 Oak Ave, Austin, TX 78702",
            "price": 325000,
            "bedrooms": 2,
            "bathrooms": 2,
            "square_footage": 1500,
            "property_type": "condo",
            "year_built": 2015,
            "estimated_rental_income": 2200,
            "appreciation_rate": 3.8,
            "school_rating": 7,
            "crime_rate": 30
        }
    ]
    
    # Apply filters
    filtered = properties
    if property_type:
        filtered = [p for p in filtered if p["property_type"] == property_type]
    if min_price:
        filtered = [p for p in filtered if p["price"] >= min_price]
    if max_price:
        filtered = [p for p in filtered if p["price"] <= max_price]
    if bedrooms:
        filtered = [p for p in filtered if p["bedrooms"] >= bedrooms]
    if bathrooms:
        filtered = [p for p in filtered if p["bathrooms"] >= bathrooms]
    
    return {
        "location": location,
        "total_results": len(filtered),
        "properties": filtered[:limit]
    }


@router.get("/{property_id}")
async def get_property_details(
    property_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed property information
    """
    # Mock property details
    property_details = {
        "id": property_id,
        "address": "123 Main St, Austin, TX 78701",
        "price": 450000,
        "bedrooms": 3,
        "bathrooms": 2.5,
        "square_footage": 2100,
        "property_type": "single_family",
        "year_built": 2005,
        "lot_size": 0.25,
        "hoa_fees": 150,
        "property_tax": 9000,
        "estimated_rental_income": 2800,
        "appreciation_rate": 4.2,
        "school_rating": 8,
        "crime_rate": 25,
        "nearby_schools": [
            {"name": "Austin Elementary", "rating": 8, "distance": 0.5},
            {"name": "Central High School", "rating": 7, "distance": 1.2}
        ],
        "neighborhood_stats": {
            "median_income": 75000,
            "unemployment_rate": 3.2,
            "population_growth": 2.5
        },
        "images": [
            "https://example.com/property1.jpg",
            "https://example.com/property2.jpg"
        ]
    }
    
    return property_details

# Made with Bob
