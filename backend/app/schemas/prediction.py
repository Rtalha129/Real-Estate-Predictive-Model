"""
Pydantic schemas for prediction requests and responses
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class PropertyType(str, Enum):
    """Property type enumeration"""
    SINGLE_FAMILY = "single_family"
    MULTI_FAMILY = "multi_family"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    COMMERCIAL = "commercial"
    LAND = "land"


class RenovationSkill(str, Enum):
    """Renovation skill level"""
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"


class RiskTolerance(str, Enum):
    """Risk tolerance level"""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class InvestmentStrategy(str, Enum):
    """Investment strategy types"""
    BUY_AND_HOLD = "buy_and_hold"
    HOUSE_FLIPPING = "house_flipping"
    AIRBNB = "airbnb"
    MULTI_FAMILY = "multi_family"
    COMMERCIAL = "commercial"
    HYBRID = "hybrid"


class PredictionInput(BaseModel):
    """Input schema for prediction request"""
    
    # User constraints
    hours_per_week: float = Field(..., ge=0, le=168, description="Hours available per week")
    investment_amount: float = Field(..., ge=0, description="Initial investment capital")
    
    # Property details
    property_type: PropertyType
    location: str = Field(..., min_length=2, description="City, State or ZIP code")
    property_price: Optional[float] = Field(None, ge=0)
    square_footage: Optional[float] = Field(None, ge=0)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[float] = Field(None, ge=0)
    property_age: Optional[int] = Field(None, ge=0)
    
    # User profile
    renovation_skill: RenovationSkill
    risk_tolerance: RiskTolerance
    
    # Financial details
    mortgage_rate: Optional[float] = Field(None, ge=0, le=20)
    down_payment_percent: Optional[float] = Field(20.0, ge=0, le=100)
    holding_period_months: int = Field(..., ge=1, le=360)
    
    # Market conditions (optional - will be fetched if not provided)
    market_appreciation_rate: Optional[float] = None
    rental_demand_score: Optional[float] = Field(None, ge=0, le=100)
    crime_rate: Optional[float] = Field(None, ge=0, le=100)
    school_rating: Optional[float] = Field(None, ge=0, le=10)
    
    @validator('hours_per_week')
    def validate_hours(cls, v):
        if v < 0 or v > 168:
            raise ValueError('Hours per week must be between 0 and 168')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "hours_per_week": 10,
                "investment_amount": 50000,
                "property_type": "single_family",
                "location": "Austin, TX",
                "property_price": 350000,
                "square_footage": 1800,
                "bedrooms": 3,
                "bathrooms": 2,
                "property_age": 15,
                "renovation_skill": "intermediate",
                "risk_tolerance": "moderate",
                "mortgage_rate": 6.5,
                "down_payment_percent": 20,
                "holding_period_months": 60
            }
        }


class PredictionOutput(BaseModel):
    """Output schema for prediction response"""
    
    # Predictions
    predicted_roi: float = Field(..., description="Expected ROI percentage")
    predicted_monthly_cashflow: float = Field(..., description="Monthly cash flow")
    predicted_appreciation: float = Field(..., description="Property appreciation")
    predicted_rental_income: Optional[float] = Field(None, description="Monthly rental income")
    predicted_flip_profit: Optional[float] = Field(None, description="Profit from flipping")
    time_to_profit_months: int = Field(..., description="Months until profitable")
    risk_score: float = Field(..., ge=0, le=100, description="Investment risk score")
    recommended_strategy: InvestmentStrategy
    
    # Analysis
    confidence_score: float = Field(..., ge=0, le=100)
    feature_importance: Dict[str, float]
    
    # Recommendations
    time_commitment_match: float = Field(..., ge=0, le=100, description="How well time matches strategy")
    alternative_strategies: List[Dict[str, Any]]
    
    # Metadata
    model_version: str
    prediction_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_roi": 15.5,
                "predicted_monthly_cashflow": 450.0,
                "predicted_appreciation": 25000.0,
                "predicted_rental_income": 2200.0,
                "predicted_flip_profit": None,
                "time_to_profit_months": 18,
                "risk_score": 35.0,
                "recommended_strategy": "buy_and_hold",
                "confidence_score": 87.5,
                "feature_importance": {
                    "hours_per_week": 0.25,
                    "investment_amount": 0.20,
                    "location": 0.18
                },
                "time_commitment_match": 92.0,
                "alternative_strategies": [],
                "model_version": "v1.0.0",
                "created_at": "2024-01-01T00:00:00"
            }
        }


class ScenarioCreate(BaseModel):
    """Schema for creating investment scenario"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    input_data: PredictionInput
    is_favorite: bool = False


class ScenarioResponse(BaseModel):
    """Schema for scenario response"""
    id: int
    name: str
    description: Optional[str]
    input_data: Dict[str, Any]
    prediction_data: Optional[Dict[str, Any]]
    is_favorite: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MarketTrendResponse(BaseModel):
    """Schema for market trend data"""
    location: str
    property_type: str
    median_price: Optional[float]
    price_per_sqft: Optional[float]
    appreciation_rate: Optional[float]
    rental_yield: Optional[float]
    vacancy_rate: Optional[float]
    days_on_market: Optional[int]
    unemployment_rate: Optional[float]
    population_growth: Optional[float]
    median_income: Optional[float]
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Made with Bob
