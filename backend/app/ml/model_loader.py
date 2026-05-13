"""
ML Model loader utility
"""
from app.ml.predictor import predictor


def load_models():
    """Load ML models on application startup"""
    predictor.load_models()
    print("ML models loaded successfully")


def get_predictor():
    """Get the global predictor instance"""
    return predictor

# Made with Bob
