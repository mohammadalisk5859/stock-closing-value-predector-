# 📈 Multi-Market Stock Price Predictor

A full-stack web application for predicting stock closing prices using machine learning. Supports multiple markets including US stocks (NASDAQ, NYSE) and Indian stocks (NSE).

## Features

- 📊 Real-time stock data fetching from Yahoo Finance
- 🤖 ML-powered price prediction using linear regression
- 📈 Interactive historical price charts
- 🌐 Support for multiple markets (US, India, etc.)
- 💻 Beautiful, responsive UI
- ⚡ Fast API endpoints
- 🔍 Stock symbol validation

## Project Structure

```
stock/
├── backend/              # Flask API server
│   ├── app.py           # Main application
│   └── requirements.txt  # Python dependencies
├── frontend/            # Web interface
│   └── index.html       # Interactive UI
└── README.md            # This file
```

## Tech Stack

**Backend:**
- Flask - Web framework
- yfinance - Stock data fetching
- scikit-learn - Machine learning
- pandas & numpy - Data processing

**Frontend:**
- HTML5 & CSS3
- JavaScript (Vanilla)
- Chart.js - Data visualization

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser

## Installation & Setup

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Open Frontend

Open `frontend/index.html` in your web browser, or serve it using a local server:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

## API Endpoints

### Predict Stock Price
**POST** `/api/predict`

Request:
```json
{
  "symbol": "AAPL",
  "days": 60
}
```

Response:
```json
{
  "current_price": 150.25,
  "predicted_price": 152.30,
  "change": 2.05,
  "change_percent": 1.36,
  "timestamp": "2026-01-14T10:30:00"
}
```

### Get Historical Data
**POST** `/api/historical`

Request:
```json
{
  "symbol": "AAPL",
  "days": 60
}
```

Response:
```json
{
  "data": [
    {
      "Date": "2026-01-13",
      "Close": 150.25,
      "Open": 149.50,
      "High": 151.00,
      "Low": 149.00,
      "Volume": 50000000
    },
    ...
  ]
}
```

### Health Check
**GET** `/api/health`

Response:
```json
{
  "status": "ok"
}
```

## Usage Examples

### US Stocks
- **AAPL** - Apple
- **GOOGL** - Google
- **MSFT** - Microsoft
- **TSLA** - Tesla
- **AMZN** - Amazon

### Indian Stocks (NSE)
- **RELIANCE.NS** - Reliance Industries
- **TCS.NS** - Tata Consultancy Services
- **INFY.NS** - Infosys
- **WIPRO.NS** - Wipro

## How Predictions Work

1. **Data Collection**: Fetches historical stock price data for the specified period
2. **Normalization**: Scales prices to 0-1 range for better model performance
3. **Training**: Trains a linear regression model on historical trends
4. **Prediction**: Predicts the next day's closing price
5. **Display**: Shows prediction with change percentage and historical chart

## Important Notes

⚠️ **Disclaimer**: Predictions are based on historical trend analysis and should not be considered as financial advice. Stock prices are influenced by many unpredictable factors including market sentiment, news, and global events. Always consult with a financial advisor before making investment decisions.

## Limitations

- Predictions use simple linear regression (can be enhanced with LSTM/Neural Networks)
- Limited to publicly available historical data
- Doesn't account for earnings reports, market events, or news
- Best used as a learning tool, not for actual trading

## Enhancement Ideas

- [ ] Implement LSTM neural networks for better predictions
- [ ] Add sentiment analysis from news/social media
- [ ] Support for technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Portfolio tracking and comparison
- [ ] User authentication and saved watchlists
- [ ] Real-time price updates via WebSockets
- [ ] Mobile app version
- [ ] Backtesting module

## Troubleshooting

**Issue**: "Could not fetch data for symbol"
- Solution: Verify the stock symbol is correct and trading on the market

**Issue**: CORS errors
- Solution: Ensure Flask backend is running and CORS is properly configured

**Issue**: Chart not displaying
- Solution: Check browser console for JavaScript errors, ensure Chart.js CDN is accessible

## License

MIT License - Feel free to use this project for learning and personal use.

## Support

For issues or questions, check the API endpoints and ensure both backend and frontend are running correctly.

Happy Investing! 📈
