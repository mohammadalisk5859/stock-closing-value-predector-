from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

def fetch_stock_data(symbol, days=60):
    """Fetch historical stock data"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        return data
    except Exception as e:
        return None

def predict_price(symbol, days=60):
    """Predict tomorrow's closing price using linear regression"""
    try:
        # Fetch data
        data = fetch_stock_data(symbol, days)
        
        if data is None or len(data) < 5:
            return None
        
        # Prepare data
        close_prices = data['Close'].values.reshape(-1, 1)
        
        # Normalize prices
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_prices = scaler.fit_transform(close_prices)
        
        # Create sequences
        X = np.arange(len(scaled_prices)).reshape(-1, 1)
        y = scaled_prices.flatten()
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next day
        next_day_idx = np.array([[len(scaled_prices)]])
        predicted_scaled = model.predict(next_day_idx)[0]
        
        # Inverse transform
        predicted_price = scaler.inverse_transform(np.array([[predicted_scaled]]))[0][0]
        
        # Get current price
        current_price = close_prices[-1][0]
        
        # Calculate change percentage
        change_percent = ((predicted_price - current_price) / current_price) * 100
        
        return {
            'current_price': float(current_price),
            'predicted_price': float(predicted_price),
            'change': float(predicted_price - current_price),
            'change_percent': float(change_percent),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error predicting price: {e}")
        return None

def get_historical_data(symbol, days=60):
    """Get historical data for chart"""
    try:
        data = fetch_stock_data(symbol, days)
        if data is None:
            return None
        
        data['Date'] = data.index.strftime('%Y-%m-%d')
        return data[['Date', 'Close', 'Open', 'High', 'Low', 'Volume']].tail(days).to_dict('records')
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for stock price prediction"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        days = data.get('days', 60)
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        prediction = predict_price(symbol, days)
        
        if prediction is None:
            return jsonify({'error': f'Could not fetch data for symbol {symbol}'}), 404
        
        return jsonify(prediction), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/historical', methods=['POST'])
def historical():
    """API endpoint for historical data"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        days = data.get('days', 60)
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        hist_data = get_historical_data(symbol, days)
        
        if hist_data is None:
            return jsonify({'error': f'Could not fetch data for symbol {symbol}'}), 404
        
        return jsonify({'data': hist_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    """Search for stock symbol"""
    try:
        query = request.args.get('q', '').upper()
        
        if not query or len(query) < 1:
            return jsonify({'results': []}), 200
        
        # Validate symbol exists by fetching a day of data
        try:
            data = yf.download(query, period='1d', progress=False)
            if len(data) > 0:
                ticker = yf.Ticker(query)
                return jsonify({
                    'results': [{
                        'symbol': query,
                        'name': ticker.info.get('longName', query)
                    }]
                }), 200
        except:
            pass
        
        return jsonify({'results': []}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
