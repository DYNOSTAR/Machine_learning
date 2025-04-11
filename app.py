from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

# 1. Function to Fetch Forex Data from Alpha Vantage API
def fetch_data(from_currency, to_currency, api_key):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'FX_INTRADAY',
        'from_symbol': from_currency,
        'to_symbol': to_currency,
        'interval': '5min',  # You can change this to 1min, 15min, etc.
        'apikey': api_key,
        'outputsize': 'full'
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Check if the request is successful
    if "Time Series FX (5min)" not in data:
        print("Error fetching data:", data)  # Log the error details
        raise ValueError(data.get('Error Message', 'Unknown error occurred while fetching data'))

    # Convert response into DataFrame
    df = pd.DataFrame.from_dict(data['Time Series FX (5min)'], orient='index')
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df


# 2. Expose fetch_data as a REST API Endpoint
@app.route('/fetch-data', methods=['POST'])
def fetch_data_endpoint():
    try:
        # Parse JSON from the request
        request_data = request.json
        from_currency = request_data.get('from_currency')
        to_currency = request_data.get('to_currency')
        api_key = request_data.get('api_key')

        # Validate inputs
        if not (from_currency and to_currency and api_key):
            return jsonify({"error": "Missing required parameters"}), 400

        # Fetch data using the fetch_data function
        df = fetch_data(from_currency, to_currency, api_key)

        # Convert DataFrame to JSON format
        data = df.reset_index().to_dict(orient='records')
        return jsonify({"data": data}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


# 3. Home Endpoint
@app.route('/')
def home():
    return "Forex Trading Bot Backend is Running"


# 4. Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
