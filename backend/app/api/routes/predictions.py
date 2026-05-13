"""
Predictions API routes
Core endpoint for real estate investment predictions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionInput, PredictionOutput
from app.ml.model_loader import get_predictor

router = APIRouter()


@router.post("/", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
async def create_prediction(
    input_data: PredictionInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new investment prediction
    
    This is the core endpoint that:
    1. Takes user input (time, capital, preferences)
    2. Engineers features with heavy time-weighting
    3. Predicts ROI, cash flow, and best strategy
    4. Returns comprehensive investment analysis
    """
    try:
        # Get predictor instance
        predictor = get_predictor()
        
        # Generate prediction
        prediction_output = predictor.predict(input_data)
        
        # Save prediction to database
        db_prediction = Prediction(
            user_id=current_user.id,
            hours_per_week=input_data.hours_per_week,
            investment_amount=input_data.investment_amount,
            property_type=input_data.property_type.value,
            location=input_data.location,
            renovation_skill=input_data.renovation_skill.value,
            risk_tolerance=input_data.risk_tolerance.value,
            holding_period_months=input_data.holding_period_months,
            property_price=input_data.property_price,
            mortgage_rate=input_data.mortgage_rate,
            down_payment_percent=input_data.down_payment_percent,
            property_age=input_data.property_age,
            square_footage=input_data.square_footage,
            bedrooms=input_data.bedrooms,
            bathrooms=input_data.bathrooms,
            market_appreciation_rate=input_data.market_appreciation_rate,
            rental_demand_score=input_data.rental_demand_score,
            crime_rate=input_data.crime_rate,
            school_rating=input_data.school_rating,
            predicted_roi=prediction_output.predicted_roi,
            predicted_monthly_cashflow=prediction_output.predicted_monthly_cashflow,
            predicted_appreciation=prediction_output.predicted_appreciation,
            predicted_rental_income=prediction_output.predicted_rental_income,
            predicted_flip_profit=prediction_output.predicted_flip_profit,
            time_to_profit_months=prediction_output.time_to_profit_months,
            risk_score=prediction_output.risk_score,
            recommended_strategy=prediction_output.recommended_strategy.value,
            feature_importance=prediction_output.feature_importance,
            confidence_score=prediction_output.confidence_score,
            model_version=prediction_output.model_version
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        # Add prediction ID to output
        prediction_output.prediction_id = db_prediction.id
        
        return prediction_output
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/history", response_model=List[dict])
async def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0
):
    """
    Get user's prediction history
    """
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(
        Prediction.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    return [
        {
            "id": p.id,
            "location": p.location,
            "property_type": p.property_type,
            "predicted_roi": p.predicted_roi,
            "recommended_strategy": p.recommended_strategy,
            "risk_score": p.risk_score,
            "created_at": p.created_at
        }
        for p in predictions
    ]


@router.get("/{prediction_id}", response_model=dict)
async def get_prediction_detail(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed prediction by ID
    """
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    return {
        "id": prediction.id,
        "input_data": {
            "hours_per_week": prediction.hours_per_week,
            "investment_amount": prediction.investment_amount,
            "property_type": prediction.property_type,
            "location": prediction.location,
            "renovation_skill": prediction.renovation_skill,
            "risk_tolerance": prediction.risk_tolerance,
            "holding_period_months": prediction.holding_period_months,
            "property_price": prediction.property_price,
            "mortgage_rate": prediction.mortgage_rate,
            "down_payment_percent": prediction.down_payment_percent
        },
        "predictions": {
            "predicted_roi": prediction.predicted_roi,
            "predicted_monthly_cashflow": prediction.predicted_monthly_cashflow,
            "predicted_appreciation": prediction.predicted_appreciation,
            "predicted_rental_income": prediction.predicted_rental_income,
            "predicted_flip_profit": prediction.predicted_flip_profit,
            "time_to_profit_months": prediction.time_to_profit_months,
            "risk_score": prediction.risk_score,
            "recommended_strategy": prediction.recommended_strategy,
            "confidence_score": prediction.confidence_score
        },
        "feature_importance": prediction.feature_importance,
        "model_version": prediction.model_version,
        "created_at": prediction.created_at
    }


@router.delete("/{prediction_id}")
async def delete_prediction(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a prediction
    """
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    db.delete(prediction)
    db.commit()
    
    return {"message": "Prediction deleted successfully"}

# Made with Bob
