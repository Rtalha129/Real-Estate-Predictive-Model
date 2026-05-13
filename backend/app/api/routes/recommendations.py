"""
AI Recommendations API routes
Personalized investment strategy recommendations
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionInput
from app.ml.model_loader import get_predictor

router = APIRouter()


@router.post("/")
async def get_recommendations(
    input_data: PredictionInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered investment recommendations
    Based on user profile and constraints
    """
    predictor = get_predictor()
    
    # Get full prediction
    prediction = predictor.predict(input_data)
    
    # Generate detailed recommendations
    recommendations = {
        "primary_recommendation": {
            "strategy": prediction.recommended_strategy.value,
            "confidence": prediction.confidence_score,
            "time_commitment_match": prediction.time_commitment_match,
            "expected_roi": prediction.predicted_roi,
            "risk_score": prediction.risk_score,
            "reasoning": _get_recommendation_reasoning(
                prediction.recommended_strategy.value,
                input_data.hours_per_week,
                input_data.investment_amount,
                input_data.renovation_skill.value
            )
        },
        "alternatives": prediction.alternative_strategies,
        "action_items": _generate_action_items(
            prediction.recommended_strategy.value,
            input_data
        ),
        "risk_mitigation": _get_risk_mitigation_strategies(
            prediction.risk_score,
            prediction.recommended_strategy.value
        ),
        "timeline": _generate_timeline(
            prediction.recommended_strategy.value,
            prediction.time_to_profit_months
        )
    }
    
    return recommendations


def _get_recommendation_reasoning(strategy: str, hours: float, capital: float, skill: str) -> str:
    """Generate reasoning for recommendation"""
    reasons = {
        "buy_and_hold": f"With {hours} hours per week available, a passive buy-and-hold strategy is ideal. "
                       f"Your ${capital:,.0f} investment can generate steady rental income with minimal time commitment.",
        
        "house_flipping": f"Your {hours} hours per week and {skill} renovation skills make you well-suited for active flipping. "
                         f"With ${capital:,.0f}, you can pursue higher-return renovation projects.",
        
        "airbnb": f"With {hours} hours per week, you can manage an Airbnb property effectively. "
                 f"This strategy offers higher returns than traditional rentals with moderate effort.",
        
        "multi_family": f"Your ${capital:,.0f} investment and {hours} hours per week allow for multi-family investing. "
                       f"This provides diversification and scalable income.",
        
        "commercial": f"With ${capital:,.0f} and {hours} hours per week, commercial real estate offers stable returns "
                     f"with professional property management.",
        
        "hybrid": f"Your {hours} hours per week and ${capital:,.0f} capital support a hybrid approach, "
                 f"combining rental income with selective value-add opportunities."
    }
    
    return reasons.get(strategy, "This strategy matches your profile and constraints.")


def _generate_action_items(strategy: str, input_data: PredictionInput) -> list:
    """Generate actionable next steps"""
    base_items = [
        "Get pre-approved for financing",
        "Research target neighborhoods",
        "Build relationships with real estate agents",
        "Set up property alerts"
    ]
    
    strategy_specific = {
        "buy_and_hold": [
            "Calculate rental income potential",
            "Review property management options",
            "Analyze cash flow scenarios"
        ],
        "house_flipping": [
            "Find reliable contractors",
            "Learn renovation cost estimation",
            "Study ARV (After Repair Value) analysis",
            "Build renovation project timeline"
        ],
        "airbnb": [
            "Research local Airbnb regulations",
            "Analyze seasonal demand patterns",
            "Plan furnishing and setup costs",
            "Create hosting strategy"
        ],
        "multi_family": [
            "Study multi-family financing options",
            "Learn tenant screening processes",
            "Understand property management",
            "Analyze unit economics"
        ],
        "commercial": [
            "Research commercial loan options",
            "Study lease structures",
            "Analyze tenant quality",
            "Review market vacancy rates"
        ]
    }
    
    return base_items + strategy_specific.get(strategy, [])


def _get_risk_mitigation_strategies(risk_score: float, strategy: str) -> list:
    """Generate risk mitigation recommendations"""
    mitigations = []
    
    if risk_score > 60:
        mitigations.extend([
            "Consider increasing down payment to reduce leverage",
            "Build larger cash reserves (6-12 months expenses)",
            "Get comprehensive insurance coverage",
            "Diversify across multiple properties if possible"
        ])
    
    if risk_score > 40:
        mitigations.extend([
            "Conduct thorough property inspections",
            "Research neighborhood trends carefully",
            "Have contingency budget for unexpected costs"
        ])
    
    strategy_specific = {
        "house_flipping": [
            "Lock in contractor bids before purchase",
            "Have exit strategy if market turns",
            "Don't over-improve for the neighborhood"
        ],
        "airbnb": [
            "Have backup plan if regulations change",
            "Maintain high occupancy through competitive pricing",
            "Build positive reviews quickly"
        ],
        "multi_family": [
            "Screen tenants thoroughly",
            "Maintain property to reduce turnover",
            "Keep units competitively priced"
        ]
    }
    
    mitigations.extend(strategy_specific.get(strategy, []))
    
    return mitigations


def _generate_timeline(strategy: str, time_to_profit: int) -> dict:
    """Generate investment timeline"""
    timelines = {
        "buy_and_hold": {
            "phase_1": {"months": "0-2", "activity": "Property search and acquisition"},
            "phase_2": {"months": "2-3", "activity": "Minor repairs and tenant placement"},
            "phase_3": {"months": f"3-{time_to_profit}", "activity": "Rental income and appreciation"},
            "phase_4": {"months": f"{time_to_profit}+", "activity": "Positive cash flow achieved"}
        },
        "house_flipping": {
            "phase_1": {"months": "0-1", "activity": "Property search and acquisition"},
            "phase_2": {"months": "1-4", "activity": "Renovation and improvements"},
            "phase_3": {"months": "4-6", "activity": "Marketing and sale"},
            "phase_4": {"months": "6", "activity": "Profit realization"}
        },
        "airbnb": {
            "phase_1": {"months": "0-2", "activity": "Property acquisition and setup"},
            "phase_2": {"months": "2-3", "activity": "Furnishing and listing creation"},
            "phase_3": {"months": "3-6", "activity": "Building reviews and occupancy"},
            "phase_4": {"months": f"6-{time_to_profit}", "activity": "Optimizing for profitability"}
        }
    }
    
    return timelines.get(strategy, {
        "phase_1": {"months": "0-3", "activity": "Acquisition"},
        "phase_2": {"months": "3-6", "activity": "Setup and optimization"},
        "phase_3": {"months": f"6-{time_to_profit}", "activity": "Income generation"},
        "phase_4": {"months": f"{time_to_profit}+", "activity": "Profitability"}
    })


@router.get("/strategies")
async def get_all_strategies(current_user: User = Depends(get_current_user)):
    """
    Get information about all investment strategies
    """
    strategies = [
        {
            "name": "Buy and Hold",
            "slug": "buy_and_hold",
            "time_required": "2-5 hours/week",
            "capital_required": "$30,000+",
            "skill_level": "Beginner",
            "risk_level": "Low",
            "expected_roi": "8-12%",
            "description": "Purchase property and rent long-term for passive income",
            "pros": ["Passive income", "Tax benefits", "Appreciation", "Low time commitment"],
            "cons": ["Tenant management", "Maintenance costs", "Market dependent"]
        },
        {
            "name": "House Flipping",
            "slug": "house_flipping",
            "time_required": "20+ hours/week",
            "capital_required": "$50,000+",
            "skill_level": "Advanced",
            "risk_level": "High",
            "expected_roi": "15-30%",
            "description": "Buy, renovate, and sell properties for profit",
            "pros": ["High returns", "Quick profits", "Active involvement"],
            "cons": ["High risk", "Time intensive", "Market timing critical"]
        },
        {
            "name": "Airbnb/Short-term Rental",
            "slug": "airbnb",
            "time_required": "8-12 hours/week",
            "capital_required": "$40,000+",
            "skill_level": "Intermediate",
            "risk_level": "Moderate",
            "expected_roi": "12-18%",
            "description": "Rent property short-term for higher income",
            "pros": ["Higher income", "Flexibility", "Personal use option"],
            "cons": ["More management", "Regulation risk", "Seasonal variation"]
        },
        {
            "name": "Multi-family Investing",
            "slug": "multi_family",
            "time_required": "10-15 hours/week",
            "capital_required": "$100,000+",
            "skill_level": "Intermediate",
            "risk_level": "Moderate",
            "expected_roi": "10-15%",
            "description": "Invest in properties with multiple rental units",
            "pros": ["Diversification", "Economies of scale", "Stable income"],
            "cons": ["Higher capital", "More tenants", "Complex management"]
        },
        {
            "name": "Commercial Real Estate",
            "slug": "commercial",
            "time_required": "5-10 hours/week",
            "capital_required": "$200,000+",
            "skill_level": "Intermediate",
            "risk_level": "Moderate",
            "expected_roi": "9-14%",
            "description": "Invest in office, retail, or industrial properties",
            "pros": ["Long leases", "Professional tenants", "Triple net leases"],
            "cons": ["High capital", "Economic sensitivity", "Longer vacancies"]
        }
    ]
    
    return {"strategies": strategies}

# Made with Bob
