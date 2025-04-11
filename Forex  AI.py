import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import alpaca_trade_api as tradeapi


# Function to get stock data
def get_stock_data(ticker, interval="1d", period="1mo"):
    """
    Fetch stock data from Yahoo Finance.
    :param ticker: Stock symbol (e.g., 'AAPL')
    :param interval: Data frequency (e.g., '1d', '5m')
    :param period: Time period for the data (e.g., '1mo', '1y')
    :return: DataFrame with stock data
    """
    data = yf.download(tickers=ticker, interval=interval, period=period)
    return data


# Function to calculate SMA and RSI
def calculate_features(data):
    # Moving Averages (SMA)
    data['SMA_10'] = data['Close'].rolling(window=10).mean()  # 10-day SMA
    data['SMA_50'] = data['Close'].rolling(window=50).mean()  # 50-day SMA

    # RSI Calculation
    data['RSI'] = calculate_rsi(data['Close'])  # Define your own RSI function

    return data


# Function to calculate RSI (Relative Strength Index)
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Function to train model and predict stock trends
def train_model(data, features):
    # Prepare the data
    X = data[features].dropna()
    y = (data['Close'].shift(-1) > data['Close']).astype(int)  # 1 if price goes up, 0 if down

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2f}")

    return model


# Function to decide whether to buy or sell based on model's prediction
def make_decision(model, data, features, current_cash, stock_price, risk_per_trade=0.02):
    """
    Decides whether to buy or sell based on model prediction and risk management.
    :param model: Trained machine learning model
    :param data: Stock data
    :param features: List of features for prediction
    :param current_cash: Current available cash for buying
    :param stock_price: Current stock price
    :param risk_per_trade: The percentage of portfolio to risk per trade (e.g., 2%)
    :return: Action (Buy, Sell, Hold)
    """
    # Prepare the most recent data for prediction
    recent_data = data[features].dropna().iloc[-1:]

    # Predict the next price movement (1 = Up, 0 = Down)
    prediction = model.predict(recent_data)

    # Risk management: Calculate position size based on risk
    position_size = (current_cash * risk_per_trade) / stock_price  # Number of shares to buy based on risk

    if prediction == 1:  # Price is predicted to go up
        return f"Buy {position_size:.0f} shares"
    elif prediction == 0:  # Price is predicted to go down
        return "Sell all shares"
    else:
        return "Hold"


# Function to execute trade using Alpaca API
def execute_trade(action, ticker, qty, api):
    """
    Executes the buy or sell action using Alpaca API
    :param action: 'Buy' or 'Sell'
    :param ticker: Stock symbol (e.g., 'AAPL')
    :param qty: Quantity of shares to buy or sell
    :param api: Alpaca API instance
    """
    if action == "Buy":
        api.submit_order(symbol=ticker, qty=qty, side='buy', type='market', time_in_force='gtc')
        print(f"Executed Buy Order: {qty} shares of {ticker}")
    elif action == "Sell":
        api.submit_order(symbol=ticker, qty=qty, side='sell', type='market', time_in_force='gtc')
        print(f"Executed Sell Order: {qty} shares of {ticker}")


# Function to implement Stop-Loss and Take-Profit orders
def manage_stop_loss_take_profit(stock_price, action, stop_loss_pct=0.05, take_profit_pct=0.10):
    """
    Adds stop-loss and take-profit conditions to the trade.
    :param stock_price: Current stock price
    :param action: Action (buy/sell)
    :param stop_loss_pct: Stop loss percentage (default: 5%)
    :param take_profit_pct: Take profit percentage (default: 10%)
    :return: Updated action with conditions for stop-loss and take-profit
    """
    if action == "Buy":
        stop_loss_price = stock_price * (1 - stop_loss_pct)
        take_profit_price = stock_price * (1 + take_profit_pct)
        print(f"Stop Loss: {stop_loss_price:.2f}, Take Profit: {take_profit_price:.2f}")
        return f"Buy with Stop-Loss at {stop_loss_price:.2f} and Take-Profit at {take_profit_price:.2f}"
    elif action == "Sell":
        print("Sell executed.")
        return "Sell executed"
    else:
        return action


# Main function to run the bot
def run_trading_bot(ticker, api_key, secret_key):
    # Alpaca API setup
    api = tradeapi.REST(api_key, secret_key, base_url='https://paper-api.alpaca.markets')

    # Step 1: Gather stock data
    data = get_stock_data(ticker, interval="1d", period="3mo")

    # Step 2: Calculate features (SMA and RSI)
    data = calculate_features(data)

    # Step 3: Train the model
    features = ['SMA_10', 'SMA_50', 'RSI']
    model = train_model(data, features)

    # Step 4: Make a decision (buy, sell, or hold) based on model's prediction and risk management
    current_cash = 10000  # Example: $10,000 for buying stock
    stock_price = data['Close'].iloc[-1]  # Last available stock price
    action = make_decision(model, data, features, current_cash, stock_price)

    # Step 5: Manage stop-loss and take-profit
    action_with_risk_management = manage_stop_loss_take_profit(stock_price, action)

    # Step 6: Execute trade
    if action_with_risk_management.startswith("Buy"):
        shares_to_buy = int(float(action_with_risk_management.split()[-2]))  # Extract shares to buy from action text
        execute_trade("Buy", ticker, shares_to_buy, api)
    elif action_with_risk_management.startswith("Sell"):
        execute_trade("Sell", ticker, 10, api)  # Selling all shares example
    else:
        print("No action taken. Holding position.")


# Run the bot with your desired ticker and Alpaca API keys
api_key = "YOUR_ALPACA_API_KEY"
secret_key = "YOUR_ALPACA_SECRET_KEY"
ticker = "AAPL"  # Example: Apple stock
run_trading_bot(ticker, api_key, secret_key)
