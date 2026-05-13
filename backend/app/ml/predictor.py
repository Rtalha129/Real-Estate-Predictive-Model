"""
ML Predictor for Real Estate Investment Analysis
Core prediction engine with time-weighted scoring
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
import joblib
import os
from datetime import datetime

from app.schemas.prediction import (
    PredictionInput, 
    PredictionOutput, 
    InvestmentStrategy,
    RenovationSkill,
    RiskTolerance
)


class RealEstatePredictor:
    """
    Main predictor class for real estate investment analysis
    Heavily weights user time availability in recommendations
    """
    
    def __init__(self, model_path: str = "../ml-model/models/"):
        self.model_path = model_path
        self.roi_model = None
        self.strategy_model = None
        self.model_version = "v1.0.0"
        self.feature_names = []
        
    def load_models(self):
        """Load trained ML models"""
        try:
            roi_model_path = os.path.join(self.model_path, "roi_model.pkl")
            strategy_model_path = os.path.join(self.model_path, "strategy_model.pkl")
            
            if os.path.exists(roi_model_path):
                self.roi_model = joblib.load(roi_model_path)
            if os.path.exists(strategy_model_path):
                self.strategy_model = joblib.load(strategy_model_path)
                
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
            print("Using fallback prediction logic")
    
    def engineer_features(self, input_data: PredictionInput) -> pd.DataFrame:
        """
        Engineer features from input data
        TIME AVAILABILITY is heavily weighted
        """
        features = {}
        
        # Core user features (HIGH WEIGHT)
        features['hours_per_week'] = input_data.hours_per_week
        features['investment_amount'] = input_data.investment_amount
        features['holding_period_months'] = input_data.holding_period_months
        
        # Time availability categories (CRITICAL FEATURE)
        features['time_low'] = 1 if input_data.hours_per_week < 5 else 0
        features['time_medium'] = 1 if 5 <= input_data.hours_per_week <= 15 else 0
        features['time_high'] = 1 if input_data.hours_per_week > 15 else 0
        
        # Time-to-capital ratio (time efficiency metric)
        features['time_capital_ratio'] = input_data.hours_per_week / (input_data.investment_amount / 10000)
        
        # Property features
        features['property_price'] = input_data.property_price or 300000
        features['square_footage'] = input_data.square_footage or 1500
        features['bedrooms'] = input_data.bedrooms or 3
        features['bathrooms'] = input_data.bathrooms or 2
        features['property_age'] = input_data.property_age or 20
        
        # Property type encoding
        property_types = ['single_family', 'multi_family', 'condo', 'townhouse', 'commercial', 'land']
        for pt in property_types:
            features[f'property_type_{pt}'] = 1 if input_data.property_type.value == pt else 0
        
        # Skill level encoding (affects time requirements)
        skill_levels = ['none', 'beginner', 'intermediate', 'advanced', 'professional']
        skill_multipliers = {'none': 0, 'beginner': 0.3, 'intermediate': 0.6, 'advanced': 0.85, 'professional': 1.0}
        features['renovation_skill_score'] = skill_multipliers.get(input_data.renovation_skill.value, 0.5)
        
        for skill in skill_levels:
            features[f'skill_{skill}'] = 1 if input_data.renovation_skill.value == skill else 0
        
        # Risk tolerance encoding
        risk_levels = ['very_low', 'low', 'moderate', 'high', 'very_high']
        risk_scores = {'very_low': 0.2, 'low': 0.4, 'moderate': 0.6, 'high': 0.8, 'very_high': 1.0}
        features['risk_score'] = risk_scores.get(input_data.risk_tolerance.value, 0.5)
        
        for risk in risk_levels:
            features[f'risk_{risk}'] = 1 if input_data.risk_tolerance.value == risk else 0
        
        # Financial features
        features['mortgage_rate'] = input_data.mortgage_rate or 6.5
        features['down_payment_percent'] = input_data.down_payment_percent or 20
        features['loan_amount'] = features['property_price'] * (1 - features['down_payment_percent'] / 100)
        features['monthly_mortgage'] = self._calculate_monthly_payment(
            features['loan_amount'],
            features['mortgage_rate'],
            input_data.holding_period_months
        )
        
        # Market features (use defaults if not provided)
        features['market_appreciation_rate'] = input_data.market_appreciation_rate or 3.5
        features['rental_demand_score'] = input_data.rental_demand_score or 65
        features['crime_rate'] = input_data.crime_rate or 30
        features['school_rating'] = input_data.school_rating or 7
        
        # Derived features
        features['price_per_sqft'] = features['property_price'] / features['square_footage']
        features['investment_to_price_ratio'] = input_data.investment_amount / features['property_price']
        
        return pd.DataFrame([features])
    
    def _calculate_monthly_payment(self, principal: float, annual_rate: float, months: int) -> float:
        """Calculate monthly mortgage payment"""
        if annual_rate == 0:
            return principal / months
        monthly_rate = annual_rate / 100 / 12
        payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        return payment
    
    def calculate_time_weighted_strategy(self, input_data: PredictionInput, features: pd.DataFrame) -> Tuple[InvestmentStrategy, float]:
        """
        CRITICAL: Calculate investment strategy based heavily on time availability
        This is the core innovation of the platform
        """
        hours = input_data.hours_per_week
        skill = input_data.renovation_skill.value
        risk = input_data.risk_tolerance.value
        capital = input_data.investment_amount
        
        # Strategy time requirements (hours per week)
        strategy_time_requirements = {
            InvestmentStrategy.BUY_AND_HOLD: 2,
            InvestmentStrategy.AIRBNB: 8,
            InvestmentStrategy.MULTI_FAMILY: 10,
            InvestmentStrategy.HOUSE_FLIPPING: 20,
            InvestmentStrategy.COMMERCIAL: 5,
            InvestmentStrategy.HYBRID: 12
        }
        
        # Strategy capital requirements
        strategy_capital_requirements = {
            InvestmentStrategy.BUY_AND_HOLD: 30000,
            InvestmentStrategy.AIRBNB: 40000,
            InvestmentStrategy.MULTI_FAMILY: 100000,
            InvestmentStrategy.HOUSE_FLIPPING: 50000,
            InvestmentStrategy.COMMERCIAL: 200000,
            InvestmentStrategy.HYBRID: 60000
        }
        
        # Strategy skill requirements
        strategy_skill_requirements = {
            InvestmentStrategy.BUY_AND_HOLD: 'none',
            InvestmentStrategy.AIRBNB: 'beginner',
            InvestmentStrategy.MULTI_FAMILY: 'intermediate',
            InvestmentStrategy.HOUSE_FLIPPING: 'advanced',
            InvestmentStrategy.COMMERCIAL: 'intermediate',
            InvestmentStrategy.HYBRID: 'intermediate'
        }
        
        # Calculate match scores for each strategy
        strategy_scores = {}
        
        for strategy in InvestmentStrategy:
            score = 100.0
            
            # TIME MATCH (50% weight - MOST IMPORTANT)
            time_required = strategy_time_requirements[strategy]
            time_diff = abs(hours - time_required)
            time_match = max(0, 100 - (time_diff * 5))  # Penalize 5 points per hour difference
            score *= (time_match / 100) * 0.5
            
            # CAPITAL MATCH (25% weight)
            capital_required = strategy_capital_requirements[strategy]
            if capital >= capital_required:
                capital_match = 100
            else:
                capital_match = (capital / capital_required) * 100
            score *= (capital_match / 100) * 0.25
            
            # SKILL MATCH (15% weight)
            skill_order = ['none', 'beginner', 'intermediate', 'advanced', 'professional']
            skill_required_idx = skill_order.index(strategy_skill_requirements[strategy])
            skill_current_idx = skill_order.index(skill)
            if skill_current_idx >= skill_required_idx:
                skill_match = 100
            else:
                skill_match = (skill_current_idx / skill_required_idx) * 100
            score *= (skill_match / 100) * 0.15
            
            # RISK MATCH (10% weight)
            risk_order = ['very_low', 'low', 'moderate', 'high', 'very_high']
            strategy_risk = {
                InvestmentStrategy.BUY_AND_HOLD: 'low',
                InvestmentStrategy.AIRBNB: 'moderate',
                InvestmentStrategy.MULTI_FAMILY: 'moderate',
                InvestmentStrategy.HOUSE_FLIPPING: 'high',
                InvestmentStrategy.COMMERCIAL: 'moderate',
                InvestmentStrategy.HYBRID: 'moderate'
            }
            risk_required_idx = risk_order.index(strategy_risk[strategy])
            risk_current_idx = risk_order.index(risk)
            risk_match = 100 - abs(risk_required_idx - risk_current_idx) * 20
            score *= (risk_match / 100) * 0.1
            
            strategy_scores[strategy] = max(0, score)
        
        # Get best strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        confidence = strategy_scores[best_strategy]
        
        return best_strategy, confidence
    
    def predict_roi(self, features: pd.DataFrame, strategy: InvestmentStrategy) -> Dict[str, float]:
        """
        Predict ROI and financial metrics
        Uses ML model if available, otherwise uses heuristics
        """
        # Base ROI by strategy
        base_roi = {
            InvestmentStrategy.BUY_AND_HOLD: 8.0,
            InvestmentStrategy.AIRBNB: 12.0,
            InvestmentStrategy.MULTI_FAMILY: 10.0,
            InvestmentStrategy.HOUSE_FLIPPING: 15.0,
            InvestmentStrategy.COMMERCIAL: 9.0,
            InvestmentStrategy.HYBRID: 11.0
        }
        
        roi = base_roi[strategy]
        
        # Adjust based on features
        market_appreciation = features['market_appreciation_rate'].values[0]
        rental_demand = features['rental_demand_score'].values[0]
        risk_score = features['risk_score'].values[0]
        
        # Market adjustment
        roi += (market_appreciation - 3.5) * 0.5
        
        # Rental demand adjustment (for rental strategies)
        if strategy in [InvestmentStrategy.BUY_AND_HOLD, InvestmentStrategy.AIRBNB, InvestmentStrategy.MULTI_FAMILY]:
            roi += (rental_demand - 50) * 0.05
        
        # Risk adjustment
        roi += (risk_score - 0.5) * 3
        
        # Calculate other metrics
        property_price = features['property_price'].values[0]
        monthly_mortgage = features['monthly_mortgage'].values[0]
        
        # Rental income estimation
        rental_income = 0
        if strategy in [InvestmentStrategy.BUY_AND_HOLD, InvestmentStrategy.AIRBNB, InvestmentStrategy.MULTI_FAMILY]:
            rental_income = property_price * 0.006  # 0.6% of property value per month
            if strategy == InvestmentStrategy.AIRBNB:
                rental_income *= 1.3  # 30% premium for Airbnb
        
        # Monthly cash flow
        monthly_cashflow = rental_income - monthly_mortgage - (property_price * 0.01 / 12)  # 1% annual expenses
        
        # Appreciation
        holding_months = features['holding_period_months'].values[0]
        appreciation = property_price * (market_appreciation / 100) * (holding_months / 12)
        
        # Flip profit (for flipping strategy)
        flip_profit = 0
        if strategy == InvestmentStrategy.HOUSE_FLIPPING:
            renovation_cost = property_price * 0.15
            after_repair_value = property_price * 1.25
            flip_profit = after_repair_value - property_price - renovation_cost
        
        # Time to profit
        if monthly_cashflow > 0:
            time_to_profit = int(features['investment_amount'].values[0] / monthly_cashflow)
        else:
            time_to_profit = holding_months
        
        return {
            'predicted_roi': round(roi, 2),
            'predicted_monthly_cashflow': round(monthly_cashflow, 2),
            'predicted_appreciation': round(appreciation, 2),
            'predicted_rental_income': round(rental_income, 2) if rental_income > 0 else None,
            'predicted_flip_profit': round(flip_profit, 2) if flip_profit > 0 else None,
            'time_to_profit_months': min(time_to_profit, holding_months)
        }
    
    def calculate_risk_score(self, input_data: PredictionInput, strategy: InvestmentStrategy) -> float:
        """Calculate investment risk score (0-100)"""
        risk_score = 50.0  # Base risk
        
        # Strategy risk
        strategy_risk = {
            InvestmentStrategy.BUY_AND_HOLD: -10,
            InvestmentStrategy.AIRBNB: 5,
            InvestmentStrategy.MULTI_FAMILY: 0,
            InvestmentStrategy.HOUSE_FLIPPING: 20,
            InvestmentStrategy.COMMERCIAL: 10,
            InvestmentStrategy.HYBRID: 5
        }
        risk_score += strategy_risk[strategy]
        
        # Market risk
        if input_data.market_appreciation_rate:
            if input_data.market_appreciation_rate < 2:
                risk_score += 15
            elif input_data.market_appreciation_rate > 5:
                risk_score -= 10
        
        # Leverage risk
        if input_data.down_payment_percent and input_data.down_payment_percent < 20:
            risk_score += 10
        
        # Time mismatch risk (CRITICAL)
        hours = input_data.hours_per_week
        if strategy == InvestmentStrategy.HOUSE_FLIPPING and hours < 15:
            risk_score += 25  # High risk if insufficient time for flipping
        elif strategy == InvestmentStrategy.BUY_AND_HOLD and hours > 20:
            risk_score -= 5  # Lower risk with more oversight
        
        return max(0, min(100, risk_score))
    
    def get_feature_importance(self, features: pd.DataFrame) -> Dict[str, float]:
        """Get feature importance scores"""
        # Hardcoded importance (would come from trained model)
        importance = {
            'hours_per_week': 0.25,  # HIGHEST WEIGHT
            'investment_amount': 0.18,
            'location': 0.15,
            'property_price': 0.12,
            'market_appreciation_rate': 0.10,
            'renovation_skill_score': 0.08,
            'risk_score': 0.07,
            'holding_period_months': 0.05
        }
        return importance
    
    def get_alternative_strategies(
        self, 
        input_data: PredictionInput, 
        primary_strategy: InvestmentStrategy,
        primary_confidence: float
    ) -> List[Dict[str, Any]]:
        """Get alternative investment strategies"""
        alternatives = []
        
        # Calculate scores for all strategies
        features = self.engineer_features(input_data)
        
        for strategy in InvestmentStrategy:
            if strategy != primary_strategy:
                _, confidence = self.calculate_time_weighted_strategy(input_data, features)
                if confidence > 40:  # Only show viable alternatives
                    predictions = self.predict_roi(features, strategy)
                    alternatives.append({
                        'strategy': strategy.value,
                        'confidence': round(confidence, 2),
                        'predicted_roi': predictions['predicted_roi'],
                        'reason': self._get_strategy_reason(strategy, input_data)
                    })
        
        # Sort by confidence
        alternatives.sort(key=lambda x: x['confidence'], reverse=True)
        return alternatives[:3]  # Top 3 alternatives
    
    def _get_strategy_reason(self, strategy: InvestmentStrategy, input_data: PredictionInput) -> str:
        """Get reason for strategy recommendation"""
        reasons = {
            InvestmentStrategy.BUY_AND_HOLD: "Low time commitment, steady passive income",
            InvestmentStrategy.AIRBNB: "Higher returns with moderate management",
            InvestmentStrategy.MULTI_FAMILY: "Scalable income with diversification",
            InvestmentStrategy.HOUSE_FLIPPING: "High returns for active investors",
            InvestmentStrategy.COMMERCIAL: "Stable long-term returns",
            InvestmentStrategy.HYBRID: "Balanced approach with flexibility"
        }
        return reasons.get(strategy, "Alternative investment approach")
    
    def predict(self, input_data: PredictionInput) -> PredictionOutput:
        """
        Main prediction method
        Returns comprehensive investment analysis
        """
        # Engineer features
        features = self.engineer_features(input_data)
        
        # Determine best strategy (TIME-WEIGHTED)
        strategy, time_commitment_match = self.calculate_time_weighted_strategy(input_data, features)
        
        # Predict financial metrics
        predictions = self.predict_roi(features, strategy)
        
        # Calculate risk
        risk_score = self.calculate_risk_score(input_data, strategy)
        
        # Get feature importance
        feature_importance = self.get_feature_importance(features)
        
        # Get alternatives
        alternatives = self.get_alternative_strategies(input_data, strategy, time_commitment_match)
        
        # Create output
        output = PredictionOutput(
            predicted_roi=predictions['predicted_roi'],
            predicted_monthly_cashflow=predictions['predicted_monthly_cashflow'],
            predicted_appreciation=predictions['predicted_appreciation'],
            predicted_rental_income=predictions['predicted_rental_income'],
            predicted_flip_profit=predictions['predicted_flip_profit'],
            time_to_profit_months=predictions['time_to_profit_months'],
            risk_score=risk_score,
            recommended_strategy=strategy,
            confidence_score=time_commitment_match,
            feature_importance=feature_importance,
            time_commitment_match=time_commitment_match,
            alternative_strategies=alternatives,
            model_version=self.model_version,
            created_at=datetime.utcnow()
        )
        
        return output


# Global predictor instance
predictor = RealEstatePredictor()

# Made with Bob
