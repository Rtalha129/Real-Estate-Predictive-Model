"""
Prediction database models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Prediction(Base):
    """Prediction model for storing ML predictions"""
    
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Input features
    hours_per_week = Column(Float, nullable=False)
    investment_amount = Column(Float, nullable=False)
    property_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    renovation_skill = Column(String, nullable=False)
    risk_tolerance = Column(String, nullable=False)
    holding_period_months = Column(Integer, nullable=False)
    
    # Property details
    property_price = Column(Float)
    mortgage_rate = Column(Float)
    down_payment_percent = Column(Float)
    property_age = Column(Integer)
    square_footage = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    
    # Market conditions
    market_appreciation_rate = Column(Float)
    rental_demand_score = Column(Float)
    crime_rate = Column(Float)
    school_rating = Column(Float)
    
    # Predictions
    predicted_roi = Column(Float)
    predicted_monthly_cashflow = Column(Float)
    predicted_appreciation = Column(Float)
    predicted_rental_income = Column(Float)
    predicted_flip_profit = Column(Float)
    time_to_profit_months = Column(Integer)
    risk_score = Column(Float)
    recommended_strategy = Column(String)
    
    # Additional data
    feature_importance = Column(JSON)
    confidence_score = Column(Float)
    model_version = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="predictions")


class InvestmentScenario(Base):
    """Saved investment scenarios"""
    
    __tablename__ = "investment_scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(String)
    
    # Scenario data (stored as JSON)
    input_data = Column(JSON, nullable=False)
    prediction_data = Column(JSON)
    
    is_favorite = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="scenarios")


class MarketData(Base):
    """Market data cache"""
    
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    location = Column(String, nullable=False, index=True)
    property_type = Column(String, nullable=False)
    
    # Market metrics
    median_price = Column(Float)
    price_per_sqft = Column(Float)
    appreciation_rate = Column(Float)
    rental_yield = Column(Float)
    vacancy_rate = Column(Float)
    days_on_market = Column(Integer)
    
    # Economic indicators
    unemployment_rate = Column(Float)
    population_growth = Column(Float)
    median_income = Column(Float)
    
    # Additional data
    data_source = Column(String)
    raw_data = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Made with Bob
