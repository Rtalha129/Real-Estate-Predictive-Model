# API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.realestatepredictorAI.com
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User

```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Login

```http
POST /api/auth/login
```

**Request Body:** (Form Data)
```
username=johndoe
password=SecurePass123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Get Current User

```http
GET /api/auth/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Predictions

#### Create Prediction

```http
POST /api/predictions/
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
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
  "holding_period_months": 60,
  "market_appreciation_rate": 4.2,
  "rental_demand_score": 75,
  "crime_rate": 25,
  "school_rating": 8
}
```

**Response:** `200 OK`
```json
{
  "predicted_roi": 15.5,
  "predicted_monthly_cashflow": 450.0,
  "predicted_appreciation": 25000.0,
  "predicted_rental_income": 2200.0,
  "predicted_flip_profit": null,
  "time_to_profit_months": 18,
  "risk_score": 35.0,
  "recommended_strategy": "buy_and_hold",
  "confidence_score": 87.5,
  "feature_importance": {
    "hours_per_week": 0.25,
    "investment_amount": 0.18,
    "location": 0.15,
    "property_price": 0.12,
    "market_appreciation_rate": 0.10
  },
  "time_commitment_match": 92.0,
  "alternative_strategies": [
    {
      "strategy": "airbnb",
      "confidence": 75.2,
      "predicted_roi": 18.3,
      "reason": "Higher returns with moderate management"
    }
  ],
  "model_version": "v1.0.0",
  "prediction_id": 123,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Get Prediction History

```http
GET /api/predictions/history?limit=10&offset=0
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 123,
    "location": "Austin, TX",
    "property_type": "single_family",
    "predicted_roi": 15.5,
    "recommended_strategy": "buy_and_hold",
    "risk_score": 35.0,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Prediction Details

```http
GET /api/predictions/{prediction_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 123,
  "input_data": {
    "hours_per_week": 10,
    "investment_amount": 50000,
    "property_type": "single_family",
    "location": "Austin, TX"
  },
  "predictions": {
    "predicted_roi": 15.5,
    "predicted_monthly_cashflow": 450.0,
    "recommended_strategy": "buy_and_hold",
    "risk_score": 35.0
  },
  "feature_importance": {},
  "model_version": "v1.0.0",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Scenarios

#### Save Scenario

```http
POST /api/scenarios/
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Austin Investment",
  "description": "3BR house in Austin",
  "input_data": {
    "hours_per_week": 10,
    "investment_amount": 50000,
    "property_type": "single_family",
    "location": "Austin, TX",
    "property_price": 350000,
    "renovation_skill": "intermediate",
    "risk_tolerance": "moderate",
    "holding_period_months": 60
  },
  "is_favorite": false
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Austin Investment",
  "description": "3BR house in Austin",
  "input_data": {},
  "prediction_data": null,
  "is_favorite": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Get All Scenarios

```http
GET /api/scenarios/?favorites_only=false
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Austin Investment",
    "description": "3BR house in Austin",
    "input_data": {},
    "prediction_data": null,
    "is_favorite": false,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### Run Prediction on Scenario

```http
POST /api/scenarios/{scenario_id}/predict
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "predicted_roi": 15.5,
  "predicted_monthly_cashflow": 450.0,
  "recommended_strategy": "buy_and_hold",
  "risk_score": 35.0
}
```

---

### Properties

#### Search Properties

```http
GET /api/properties/search?location=Austin,TX&property_type=single_family&min_price=200000&max_price=500000&bedrooms=3&limit=20
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "location": "Austin, TX",
  "total_results": 2,
  "properties": [
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
    }
  ]
}
```

#### Get Property Details

```http
GET /api/properties/{property_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
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
  "nearby_schools": [],
  "neighborhood_stats": {},
  "images": []
}
```

---

### Market Data

#### Get Market Trends

```http
GET /api/market/trends?location=Austin,TX&property_type=single_family
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "location": "Austin, TX",
  "property_type": "single_family",
  "median_price": 425000,
  "price_per_sqft": 250,
  "appreciation_rate": 4.2,
  "rental_yield": 5.8,
  "vacancy_rate": 4.5,
  "days_on_market": 35,
  "unemployment_rate": 3.2,
  "population_growth": 2.5,
  "median_income": 75000,
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Get Market Forecast

```http
GET /api/market/forecast?location=Austin,TX&months=12
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "location": "Austin, TX",
  "forecast_months": 12,
  "forecast": [
    {
      "month": 1,
      "predicted_median_price": 428500,
      "confidence_lower": 407075,
      "confidence_upper": 449925
    }
  ]
}
```

---

### Recommendations

#### Get AI Recommendations

```http
POST /api/recommendations/
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:** (Same as prediction input)

**Response:** `200 OK`
```json
{
  "primary_recommendation": {
    "strategy": "buy_and_hold",
    "confidence": 87.5,
    "time_commitment_match": 92.0,
    "expected_roi": 15.5,
    "risk_score": 35.0,
    "reasoning": "With 10 hours per week available, a passive buy-and-hold strategy is ideal..."
  },
  "alternatives": [],
  "action_items": [
    "Get pre-approved for financing",
    "Research target neighborhoods",
    "Calculate rental income potential"
  ],
  "risk_mitigation": [
    "Conduct thorough property inspections",
    "Research neighborhood trends carefully"
  ],
  "timeline": {
    "phase_1": {"months": "0-2", "activity": "Property search and acquisition"},
    "phase_2": {"months": "2-3", "activity": "Minor repairs and tenant placement"}
  }
}
```

#### Get All Strategies

```http
GET /api/recommendations/strategies
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "strategies": [
    {
      "name": "Buy and Hold",
      "slug": "buy_and_hold",
      "time_required": "2-5 hours/week",
      "capital_required": "$30,000+",
      "skill_level": "Beginner",
      "risk_level": "Low",
      "expected_roi": "8-12%",
      "description": "Purchase property and rent long-term for passive income",
      "pros": ["Passive income", "Tax benefits", "Appreciation"],
      "cons": ["Tenant management", "Maintenance costs"]
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "message": "Error details (development only)"
}
```

---

## Rate Limiting

- **Rate Limit:** 100 requests per minute per user
- **Headers:**
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

---

## Pagination

List endpoints support pagination:

```
?limit=20&offset=0
```

- `limit`: Number of items per page (default: 20, max: 100)
- `offset`: Number of items to skip (default: 0)

---

## Webhooks (Future Feature)

Subscribe to events:
- `prediction.created`
- `scenario.saved`
- `market.updated`

---

## SDKs

### Python
```python
from real_estate_api import Client

client = Client(api_key="your_api_key")
prediction = client.predictions.create({
    "hours_per_week": 10,
    "investment_amount": 50000,
    # ...
})
```

### JavaScript
```javascript
import { RealEstateClient } from '@real-estate-api/client';

const client = new RealEstateClient({ apiKey: 'your_api_key' });
const prediction = await client.predictions.create({
  hoursPerWeek: 10,
  investmentAmount: 50000,
  // ...
});
```

---

## Support

- **Email:** api-support@realestatepredictorAI.com
- **Docs:** https://docs.realestatepredictorAI.com
- **Status:** https://status.realestatepredictorAI.com