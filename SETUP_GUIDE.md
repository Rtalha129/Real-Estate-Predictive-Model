# Real Estate Investment Predictor - Setup Guide

## 🚀 Quick Start

This guide will help you set up and run the AI-powered Real Estate Investment Predictor platform.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker** (Optional) - [Download](https://www.docker.com/products/docker-desktop)

## 📁 Project Structure

```
real-estate-predictor/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Config, security, database
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── ml/          # ML predictor
│   │   └── services/    # Business logic
│   ├── main.py          # FastAPI app entry
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── store/       # State management
│   │   └── types/       # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── ml-model/            # ML training scripts
│   ├── train_model.py   # Model training
│   ├── models/          # Trained models
│   └── requirements.txt
├── data/                # Datasets
├── docs/                # Documentation
├── tests/               # Test files
├── docker-compose.yml   # Docker setup
└── README.md
```

## 🔧 Installation Methods

### Method 1: Docker (Recommended)

The easiest way to run the entire stack:

```bash
# 1. Clone the repository
git clone <repository-url>
cd real-estate-predictor

# 2. Create environment file
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# 3. Start all services
docker-compose up -d

# 4. Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Method 2: Manual Setup

#### Step 1: Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE real_estate_predictor;
\q
```

#### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials and API keys

# Initialize database
python -c "from app.core.database import init_db; init_db()"

# Run the backend
uvicorn main:app --reload
```

Backend will be available at: http://localhost:8000

#### Step 3: Train ML Models

```bash
# Navigate to ml-model directory
cd ml-model

# Install ML dependencies
pip install -r requirements.txt

# Train models (generates synthetic data if needed)
python train_model.py

# Models will be saved to ml-model/models/
```

#### Step 4: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:5173

## 🔑 Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/real_estate_predictor
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=real_estate_predictor
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (Optional - for real data)
ZILLOW_API_KEY=your-zillow-api-key
REDFIN_API_KEY=your-redfin-api-key
CENSUS_API_KEY=your-census-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# ML Model
MODEL_PATH=../ml-model/models/
MODEL_VERSION=v1.0.0

# Environment
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 📊 Using the Application

### 1. Register an Account

- Navigate to http://localhost:5173
- Click "Sign Up"
- Create your account

### 2. Make Your First Prediction

1. **Input Your Details:**
   - Hours per week available
   - Investment capital
   - Property preferences
   - Risk tolerance
   - Renovation skill level

2. **Get AI Recommendations:**
   - Expected ROI
   - Monthly cash flow
   - Best investment strategy
   - Risk analysis
   - Alternative strategies

3. **Save Scenarios:**
   - Save different investment scenarios
   - Compare multiple properties
   - Track your portfolio

### 3. Explore Features

- **Dashboard:** Overview of your predictions
- **Calculator:** Interactive investment calculator
- **Market Analysis:** Real estate market trends
- **Recommendations:** AI-powered strategy suggestions
- **Portfolio:** Track saved investments

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

### ML Model Tests

```bash
cd ml-model
python -m pytest tests/
```

## 🚀 Deployment

### Deploy to AWS

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Deploy backend (example using Elastic Beanstalk)
cd backend
eb init -p python-3.11 real-estate-api
eb create production
eb deploy
```

### Deploy to Vercel (Frontend)

```bash
cd frontend
npm install -g vercel
vercel login
vercel deploy --prod
```

### Deploy with Docker

```bash
# Build images
docker-compose build

# Push to registry
docker tag real-estate-api:latest your-registry/real-estate-api:latest
docker push your-registry/real-estate-api:latest

# Deploy to your cloud provider
```

## 🔍 API Documentation

Once the backend is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

```
POST /api/auth/register          # Register new user
POST /api/auth/login             # Login
GET  /api/auth/me                # Get current user

POST /api/predictions/           # Create prediction
GET  /api/predictions/history    # Get prediction history
GET  /api/predictions/{id}       # Get prediction details

POST /api/scenarios/             # Save scenario
GET  /api/scenarios/             # Get all scenarios
PUT  /api/scenarios/{id}         # Update scenario

GET  /api/properties/search      # Search properties
GET  /api/market/trends          # Get market trends
POST /api/recommendations/       # Get AI recommendations
```

## 🎯 Key Features Implemented

### ✅ Backend (FastAPI)
- JWT authentication
- RESTful API endpoints
- PostgreSQL database with SQLAlchemy
- Pydantic validation
- CORS middleware
- Error handling

### ✅ Machine Learning
- **Time-weighted prediction algorithm** (CORE INNOVATION)
- XGBoost regression for ROI prediction
- Strategy classification model
- Feature engineering pipeline
- Model training script with synthetic data
- SHAP explainability (ready to integrate)

### ✅ Database Models
- User authentication
- Prediction history
- Investment scenarios
- Market data caching

### ✅ AI Recommendation Engine
- Personalized strategy recommendations
- Time commitment matching
- Risk assessment
- Alternative strategy suggestions
- Action items generation
- Timeline planning

### ✅ Deployment
- Docker configuration
- Docker Compose for full stack
- Environment variable management
- Production-ready setup

## 🔧 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Verify database exists
psql -U postgres -l | grep real_estate_predictor
```

### Port Already in Use

```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Next Steps

1. **Train with Real Data:**
   - Integrate Zillow/Redfin APIs
   - Collect historical property data
   - Retrain models with real data

2. **Add Advanced Features:**
   - Monte Carlo simulations
   - Market crash stress testing
   - Reinforcement learning
   - Mobile app

3. **Enhance UI:**
   - Complete React dashboard
   - Add interactive charts
   - Implement dark mode
   - Add property maps

4. **Production Optimization:**
   - Add Redis caching
   - Implement rate limiting
   - Set up monitoring
   - Add logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file

## 🆘 Support

- **Documentation:** See `/docs` folder
- **Issues:** GitHub Issues
- **Email:** support@realestatepredictorAI.com

---

**Built with ❤️ for smart real estate investors**