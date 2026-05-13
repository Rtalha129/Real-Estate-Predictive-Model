"""
ML Model Training Script
Train XGBoost models for real estate investment prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import xgboost as xgb
import joblib
import os
from datetime import datetime
import json


class RealEstateModelTrainer:
    """Train and evaluate real estate prediction models"""
    
    def __init__(self, data_path='../data/training_data.csv'):
        self.data_path = data_path
        self.roi_model = None
        self.strategy_model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = []
        
    def load_data(self):
        """Load and prepare training data"""
        print("Loading training data...")
        
        # Check if data file exists
        if not os.path.exists(self.data_path):
            print(f"Data file not found at {self.data_path}")
            print("Generating synthetic training data...")
            self.generate_synthetic_data()
        
        df = pd.read_csv(self.data_path)
        print(f"Loaded {len(df)} training samples")
        return df
    
    def generate_synthetic_data(self, n_samples=5000):
        """Generate synthetic training data for initial model"""
        print(f"Generating {n_samples} synthetic training samples...")
        
        np.random.seed(42)
        
        data = {
            # User features
            'hours_per_week': np.random.uniform(1, 40, n_samples),
            'investment_amount': np.random.uniform(20000, 500000, n_samples),
            'holding_period_months': np.random.randint(12, 240, n_samples),
            
            # Property features
            'property_price': np.random.uniform(150000, 1000000, n_samples),
            'square_footage': np.random.uniform(800, 4000, n_samples),
            'bedrooms': np.random.randint(1, 6, n_samples),
            'bathrooms': np.random.uniform(1, 4, n_samples),
            'property_age': np.random.randint(0, 100, n_samples),
            
            # Market features
            'market_appreciation_rate': np.random.uniform(1, 8, n_samples),
            'rental_demand_score': np.random.uniform(30, 95, n_samples),
            'crime_rate': np.random.uniform(10, 80, n_samples),
            'school_rating': np.random.uniform(3, 10, n_samples),
            
            # Financial features
            'mortgage_rate': np.random.uniform(3, 8, n_samples),
            'down_payment_percent': np.random.uniform(10, 40, n_samples),
            
            # Skill and risk
            'renovation_skill_score': np.random.uniform(0, 1, n_samples),
            'risk_score': np.random.uniform(0, 1, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generate target variables based on features
        # ROI calculation (simplified)
        df['roi'] = (
            5 +  # Base ROI
            df['market_appreciation_rate'] * 0.8 +
            (df['rental_demand_score'] / 20) +
            (df['hours_per_week'] / 10) * df['renovation_skill_score'] * 2 +
            df['risk_score'] * 3 -
            (df['crime_rate'] / 30) +
            np.random.normal(0, 2, n_samples)  # Noise
        )
        
        # Strategy assignment based on time availability
        def assign_strategy(row):
            hours = row['hours_per_week']
            skill = row['renovation_skill_score']
            capital = row['investment_amount']
            
            if hours < 5:
                return 'buy_and_hold'
            elif hours < 10 and capital < 100000:
                return 'buy_and_hold'
            elif hours < 10 and capital >= 100000:
                return 'multi_family'
            elif hours < 15 and skill > 0.5:
                return 'airbnb'
            elif hours >= 20 and skill > 0.7:
                return 'house_flipping'
            elif capital >= 200000:
                return 'commercial'
            else:
                return 'hybrid'
        
        df['recommended_strategy'] = df.apply(assign_strategy, axis=1)
        
        # Save synthetic data
        os.makedirs('../data', exist_ok=True)
        df.to_csv(self.data_path, index=False)
        print(f"Synthetic data saved to {self.data_path}")
        
        return df
    
    def engineer_features(self, df):
        """Engineer features from raw data"""
        print("Engineering features...")
        
        # Time-based features
        df['time_low'] = (df['hours_per_week'] < 5).astype(int)
        df['time_medium'] = ((df['hours_per_week'] >= 5) & (df['hours_per_week'] <= 15)).astype(int)
        df['time_high'] = (df['hours_per_week'] > 15).astype(int)
        
        # Derived features
        df['price_per_sqft'] = df['property_price'] / df['square_footage']
        df['investment_to_price_ratio'] = df['investment_amount'] / df['property_price']
        df['time_capital_ratio'] = df['hours_per_week'] / (df['investment_amount'] / 10000)
        
        # Loan calculations
        df['loan_amount'] = df['property_price'] * (1 - df['down_payment_percent'] / 100)
        
        return df
    
    def prepare_features(self, df, target_col):
        """Prepare features and target for training"""
        # Select feature columns
        feature_cols = [
            'hours_per_week', 'investment_amount', 'holding_period_months',
            'property_price', 'square_footage', 'bedrooms', 'bathrooms', 'property_age',
            'market_appreciation_rate', 'rental_demand_score', 'crime_rate', 'school_rating',
            'mortgage_rate', 'down_payment_percent', 'renovation_skill_score', 'risk_score',
            'time_low', 'time_medium', 'time_high',
            'price_per_sqft', 'investment_to_price_ratio', 'time_capital_ratio', 'loan_amount'
        ]
        
        X = df[feature_cols]
        y = df[target_col]
        
        self.feature_names = feature_cols
        
        return X, y
    
    def train_roi_model(self, X, y):
        """Train XGBoost regression model for ROI prediction"""
        print("\nTraining ROI prediction model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define model
        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        
        # Hyperparameter tuning
        param_grid = {
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.15],
            'n_estimators': [100, 200, 300]
        }
        
        print("Performing hyperparameter tuning...")
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1
        )
        grid_search.fit(X_train_scaled, y_train)
        
        # Best model
        self.roi_model = grid_search.best_estimator_
        print(f"Best parameters: {grid_search.best_params_}")
        
        # Evaluate
        y_pred = self.roi_model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"ROI Model Performance:")
        print(f"  MSE: {mse:.4f}")
        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: {np.sqrt(mse):.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.roi_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10))
        
        return self.roi_model
    
    def train_strategy_model(self, X, y):
        """Train XGBoost classifier for strategy recommendation"""
        print("\nTraining strategy recommendation model...")
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )
        
        # Use same scaler as ROI model
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define model
        model = xgb.XGBClassifier(
            objective='multi:softmax',
            num_class=len(self.label_encoder.classes_),
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        # Train
        model.fit(X_train_scaled, y_train)
        self.strategy_model = model
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        
        print(f"\nStrategy Model Performance:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_
        ))
        
        return self.strategy_model
    
    def save_models(self, output_dir='models'):
        """Save trained models"""
        print(f"\nSaving models to {output_dir}/...")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save models
        joblib.dump(self.roi_model, f'{output_dir}/roi_model.pkl')
        joblib.dump(self.strategy_model, f'{output_dir}/strategy_model.pkl')
        joblib.dump(self.scaler, f'{output_dir}/scaler.pkl')
        joblib.dump(self.label_encoder, f'{output_dir}/label_encoder.pkl')
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'feature_names': self.feature_names,
            'strategy_classes': self.label_encoder.classes_.tolist(),
            'model_version': 'v1.0.0'
        }
        
        with open(f'{output_dir}/metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Models saved successfully!")
    
    def train(self):
        """Main training pipeline"""
        print("=" * 60)
        print("Real Estate Investment Predictor - Model Training")
        print("=" * 60)
        
        # Load data
        df = self.load_data()
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Train ROI model
        X, y_roi = self.prepare_features(df, 'roi')
        self.train_roi_model(X, y_roi)
        
        # Train strategy model
        X, y_strategy = self.prepare_features(df, 'recommended_strategy')
        self.train_strategy_model(X, y_strategy)
        
        # Save models
        self.save_models()
        
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("=" * 60)


if __name__ == "__main__":
    trainer = RealEstateModelTrainer()
    trainer.train()

# Made with Bob
