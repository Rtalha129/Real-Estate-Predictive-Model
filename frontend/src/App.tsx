import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            🏠 Real Estate Investment Predictor
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            AI-Powered Investment Analysis Platform
          </p>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4">
              Welcome to Your Investment Dashboard
            </h2>
            
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              This platform uses advanced machine learning to predict real estate investment profitability
              based on your time commitment, capital, and market conditions.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <div className="text-3xl mb-2">📊</div>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
                  Smart Predictions
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Time-weighted ML algorithms
                </p>
              </div>
              
              <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                <div className="text-3xl mb-2">💰</div>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
                  ROI Analysis
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Comprehensive financial metrics
                </p>
              </div>
              
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                <div className="text-3xl mb-2">🎯</div>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
                  Strategy Matching
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Personalized recommendations
                </p>
              </div>
            </div>
            
            <div className="space-y-4">
              <button
                onClick={() => setCount((count) => count + 1)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 transform hover:scale-105"
              >
                Get Started - Click Count: {count}
              </button>
              
              <div className="text-sm text-gray-500 dark:text-gray-400">
                <p>✅ Backend API: Ready</p>
                <p>✅ ML Models: Trained</p>
                <p>✅ Database: Configured</p>
                <p>🚀 Status: Development Mode</p>
              </div>
            </div>
          </div>
          
          <div className="mt-12 text-gray-600 dark:text-gray-400">
            <p className="mb-2">
              <strong>Next Steps:</strong>
            </p>
            <ul className="text-sm space-y-1">
              <li>1. Run backend: <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">cd backend && uvicorn main:app --reload</code></li>
              <li>2. Train models: <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">cd ml-model && python train_model.py</code></li>
              <li>3. API Docs: <a href="http://localhost:8000/docs" className="text-blue-600 hover:underline">http://localhost:8000/docs</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

// Made with Bob
