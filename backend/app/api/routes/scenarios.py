"""
Investment Scenarios API routes
Save and manage investment scenarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.prediction import InvestmentScenario
from app.schemas.prediction import ScenarioCreate, ScenarioResponse

router = APIRouter()


@router.post("/", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario_data: ScenarioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save a new investment scenario
    """
    scenario = InvestmentScenario(
        user_id=current_user.id,
        name=scenario_data.name,
        description=scenario_data.description,
        input_data=scenario_data.input_data.model_dump(),
        is_favorite=scenario_data.is_favorite
    )
    
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    
    return ScenarioResponse.model_validate(scenario)


@router.get("/", response_model=List[ScenarioResponse])
async def get_scenarios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    favorites_only: bool = False
):
    """
    Get all saved scenarios for current user
    """
    query = db.query(InvestmentScenario).filter(
        InvestmentScenario.user_id == current_user.id
    )
    
    if favorites_only:
        query = query.filter(InvestmentScenario.is_favorite == True)
    
    scenarios = query.order_by(InvestmentScenario.created_at.desc()).all()
    
    return [ScenarioResponse.model_validate(s) for s in scenarios]


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific scenario by ID
    """
    scenario = db.query(InvestmentScenario).filter(
        InvestmentScenario.id == scenario_id,
        InvestmentScenario.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    return ScenarioResponse.model_validate(scenario)


@router.put("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: int,
    scenario_data: ScenarioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing scenario
    """
    scenario = db.query(InvestmentScenario).filter(
        InvestmentScenario.id == scenario_id,
        InvestmentScenario.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    scenario.name = scenario_data.name
    scenario.description = scenario_data.description
    scenario.input_data = scenario_data.input_data.model_dump()
    scenario.is_favorite = scenario_data.is_favorite
    
    db.commit()
    db.refresh(scenario)
    
    return ScenarioResponse.model_validate(scenario)


@router.patch("/{scenario_id}/favorite")
async def toggle_favorite(
    scenario_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle favorite status of a scenario
    """
    scenario = db.query(InvestmentScenario).filter(
        InvestmentScenario.id == scenario_id,
        InvestmentScenario.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    scenario.is_favorite = not scenario.is_favorite
    db.commit()
    
    return {"is_favorite": scenario.is_favorite}


@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a scenario
    """
    scenario = db.query(InvestmentScenario).filter(
        InvestmentScenario.id == scenario_id,
        InvestmentScenario.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    db.delete(scenario)
    db.commit()
    
    return {"message": "Scenario deleted successfully"}


@router.post("/{scenario_id}/predict")
async def predict_scenario(
    scenario_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Run prediction on a saved scenario
    """
    from app.schemas.prediction import PredictionInput
    from app.ml.model_loader import get_predictor
    
    scenario = db.query(InvestmentScenario).filter(
        InvestmentScenario.id == scenario_id,
        InvestmentScenario.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    # Convert stored data to PredictionInput
    input_data = PredictionInput(**scenario.input_data)
    
    # Get prediction
    predictor = get_predictor()
    prediction_output = predictor.predict(input_data)
    
    # Update scenario with prediction data
    scenario.prediction_data = prediction_output.model_dump()
    db.commit()
    
    return prediction_output

# Made with Bob
