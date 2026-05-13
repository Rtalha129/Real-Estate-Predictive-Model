"""
Market Data API routes
Real estate market trends and statistics
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.prediction import MarketData
from app.schemas.prediction import MarketTrendResponse

router = APIRouter()


@router.get("/trends")
async def get_market_trends(
    location: str = Query(..., description="City, State or ZIP code"),
    property_type: Optional[str] = Query("single_family"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get market trends for a location
    """
    # Check if we have cached data
    market_data = db.query(MarketData).filter(
        MarketData.location == location,
        MarketData.property_type == property_type
    ).first()
    
    if market_data:
        return MarketTrendResponse.model_validate(market_data)
    
    # Mock market data (would fetch from external APIs)
    mock_data = {
        "location": location,
        "property_type": property_type,
        "median_price": 425000,
        "price_per_sqft": 250,
        "appreciation_rate": 4.2,
        "rental_yield": 5.8,
        "vacancy_rate": 4.5,
        "days_on_market": 35,
        "unemployment_rate": 3.2,
        "population_growth": 2.5,
        "median_income": 75000
    }
    
    # Save to cache
    new_market_data = MarketData(
        location=location,
        property_type=property_type,
        median_price=mock_data["median_price"],
        price_per_sqft=mock_data["price_per_sqft"],
        appreciation_rate=mock_data["appreciation_rate"],
        rental_yield=mock_data["rental_yield"],
        vacancy_rate=mock_data["vacancy_rate"],
        days_on_market=mock_data["days_on_market"],
        unemployment_rate=mock_data["unemployment_rate"],
        population_growth=mock_data["population_growth"],
        median_income=mock_data["median_income"],
        data_source="mock"
    )
    
    db.add(new_market_data)
    db.commit()
    db.refresh(new_market_data)
    
    return MarketTrendResponse.model_validate(new_market_data)


@router.get("/heatmap")
async def get_market_heatmap(
    state: str = Query(..., description="State abbreviation (e.g., TX, CA)"),
    metric: str = Query("appreciation_rate", description="Metric to visualize"),
    current_user: User = Depends(get_current_user)
):
    """
    Get market heatmap data for visualization
    """
    # Mock heatmap data
    cities = [
        {"city": "Austin", "value": 4.2, "lat": 30.2672, "lng": -97.7431},
        {"city": "Houston", "value": 3.8, "lat": 29.7604, "lng": -95.3698},
        {"city": "Dallas", "value": 4.5, "lat": 32.7767, "lng": -96.7970},
        {"city": "San Antonio", "value": 3.5, "lat": 29.4241, "lng": -98.4936}
    ]
    
    return {
        "state": state,
        "metric": metric,
        "data": cities
    }


@router.get("/forecast")
async def get_market_forecast(
    location: str = Query(...),
    months: int = Query(12, ge=1, le=60),
    current_user: User = Depends(get_current_user)
):
    """
    Get market forecast for future months
    """
    import random
    
    # Mock forecast data
    base_price = 425000
    forecast = []
    
    for i in range(months):
        # Simple linear growth with noise
        growth = 1 + (0.04 / 12) * (i + 1)  # 4% annual growth
        noise = random.uniform(-0.02, 0.02)
        price = base_price * growth * (1 + noise)
        
        forecast.append({
            "month": i + 1,
            "predicted_median_price": round(price, 2),
            "confidence_lower": round(price * 0.95, 2),
            "confidence_upper": round(price * 1.05, 2)
        })
    
    return {
        "location": location,
        "forecast_months": months,
        "forecast": forecast
    }


@router.get("/comparisons")
async def compare_markets(
    locations: str = Query(..., description="Comma-separated locations"),
    current_user: User = Depends(get_current_user)
):
    """
    Compare multiple markets
    """
    location_list = [loc.strip() for loc in locations.split(",")]
    
    comparisons = []
    for loc in location_list[:5]:  # Limit to 5 locations
        comparisons.append({
            "location": loc,
            "median_price": 425000,
            "appreciation_rate": 4.2,
            "rental_yield": 5.8,
            "roi_score": 7.5,
            "risk_score": 35
        })
    
    return {
        "locations": location_list,
        "comparisons": comparisons
    }

# Made with Bob
