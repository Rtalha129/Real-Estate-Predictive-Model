# AI-Powered Real Estate Investment Predictor

A full-stack machine learning platform that predicts real estate investment profitability based on user time commitment, capital, market conditions, and property characteristics.

## 🎯 Core Features

- **Time-Based Investment Predictions**: ML model that factors in user's available time per week
- **Multi-Strategy Recommendations**: Buy-and-hold, flipping, Airbnb, multi-family, commercial
- **Advanced Analytics**: Monte Carlo simulations, stress testing, scenario forecasting
- **Real-Time Market Data**: Integration with Zillow, Redfin, Census APIs
- **Interactive Dashboard**: Modern React UI with charts, heatmaps, and analytics
- **AI Recommendation Engine**: Personalized investment strategies based on user profile

## 🏗️ Architecture

```
├── frontend/          # React + Vite + TypeScript + TailwindCSS
├── backend/           # FastAPI (Python) REST API
├── ml-model/          # Machine Learning pipeline (Scikit-learn, XGBoost)
├── data/              # Datasets and ETL pipelines
├── docs/              # Documentation
└── tests/             # Unit and integration tests
```

## 🚀 Tech Stack

### Frontend
- React 18 + Vite
- TypeScript
- TailwindCSS
- Recharts / Chart.js
- Axios
- React Router

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- Prisma ORM
- JWT Authentication
- Pydantic

### Machine Learning
- Scikit-learn
- XGBoost
- Pandas
- NumPy
- SHAP (explainability)
- Joblib (model persistence)

### DevOps
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- AWS 

## 📊 ML Model Features

The model predicts investment profitability using:

### User Inputs
- Hours per week available
- Initial investment capital
- Property type
- Geographic market
- Renovation skill level
- Risk tolerance
- Financing details
- Holding period

### Market Data
- Property prices
- Mortgage rates
- Market appreciation trends
- Crime rates
- School ratings
- Rental demand
- Local economic indicators
- Property taxes
- HOA fees
- Distance to city centers

### Predictions
- Expected ROI
- Monthly cash flow
- Appreciation potential
- Rental income
- Flip profitability
- Time-to-profit
- Investment risk score
- Best strategy recommendation

## 🔧 Installation

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Docker (optional)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd real-estate-predictor
```

2. **Set up Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure database and API keys in .env
python -m uvicorn main:app --reload
```

3. **Set up Frontend**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

4. **Train ML Model**
```bash
cd ml-model
python train_model.py
```

### Docker Setup
```bash
docker-compose up -d
```

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

```
POST /api/predict              # Get investment prediction
POST /api/auth/register        # User registration
POST /api/auth/login           # User login
GET  /api/properties           # Search properties
GET  /api/market-trends        # Market data
POST /api/scenarios/save       # Save investment scenario
GET  /api/scenarios            # Get saved scenarios
POST /api/recommendations      # Get AI recommendations
```

## 🎨 Frontend Pages

- **Dashboard**: Overview with key metrics and charts
- **Property Calculator**: Interactive investment calculator
- **Market Analysis**: Heatmaps and trend visualizations
- **Recommendations**: AI-powered strategy suggestions
- **Portfolio**: Track saved investments
- **Settings**: User preferences and profile

## 🧠 ML Model Details

### Training Pipeline
1. Data collection from multiple sources
2. Feature engineering and normalization
3. Train/test split (80/20)
4. Hyperparameter tuning with GridSearchCV
5. Model validation with cross-validation
6. SHAP explainability analysis

### Models Used
- **Regression**: XGBoost for ROI prediction
- **Classification**: Random Forest for strategy recommendation
- **Time Series**: ARIMA for market trends

### Key Innovation: Time-Weighted Scoring

The model heavily weights user time availability:
- **Low time (< 5 hrs/week)**: Passive strategies (buy-and-hold)
- **Medium time (5-15 hrs/week)**: Hybrid strategies (rental management)
- **High time (> 15 hrs/week)**: Active strategies (flipping, development)

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Environment variable management
- SQL injection prevention
- Rate limiting

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# ML model tests
cd ml-model
python -m pytest tests/
```

## 📈 Performance

- API response time: < 200ms
- ML prediction time: < 500ms
- Frontend load time: < 2s
- Database query optimization with indexes

## 🌐 Deployment

### AWS Deployment
```bash
# Configure AWS credentials
aws configure

# Deploy with CDK/CloudFormation
cd infrastructure
cdk deploy
```


### Vercel (Frontend)
```bash
cd frontend
vercel deploy --prod
```

## 📊 Sample Data

Sample datasets are included in `data/samples/`:
- `housing_data.csv`: Historical property data
- `market_trends.csv`: Market indicators
- `user_scenarios.json`: Example user inputs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Zillow API for property data
- Redfin for market insights
- Census Bureau for demographic data
- Kaggle housing datasets

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: support@realestatepredictorAI.com
- Documentation: [Full docs](./docs)

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Reinforcement learning for adaptive recommendations
- [ ] Collaborative filtering
- [ ] Real-time property alerts
- [ ] Integration with MLS data
- [ ] Blockchain-based property verification
- [ ] Multi-language support

---

Built with ❤️ for smart real estate investors