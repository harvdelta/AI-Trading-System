import requests
from datetime import datetime, timedelta
import pytz

def get_btc_spot_price():
    """
    Fetch current BTC spot price from Delta Exchange.
    Returns: float - Current BTC price in USDT
    """
    try:
        url = "https://api.delta.exchange/v2/products"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('result', [])
        
        # Find BTCUSDT spot product
        for product in products:
            if product.get('symbol') == 'BTCUSDT' and product.get('product_type') == 'spot':
                mark_price = product.get('mark_price')
                if mark_price:
                    return float(mark_price)
        
        # Fallback: try to find any BTC product
        for product in products:
            symbol = product.get('symbol', '')
            if 'BTC' in symbol and 'USDT' in symbol:
                mark_price = product.get('mark_price')
                if mark_price:
                    return float(mark_price)
        
        raise Exception("BTCUSDT product not found")
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error fetching BTC price: {str(e)}")
    except (KeyError, ValueError, TypeError) as e:
        raise Exception(f"Data parsing error: {str(e)}")

def get_nearest_daily_expiry():
    """
    Get the nearest daily BTC options expiry date.
    Returns: string - Date in YYYY-MM-DD format
    """
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_tz)
    
    # BTC options typically expire at 4:30 PM IST
    expiry_time = current_time.replace(hour=16, minute=30, second=0, microsecond=0)
    
    # If current time is past today's expiry, use tomorrow
    if current_time > expiry_time:
        expiry_date = current_time.date() + timedelta(days=1)
    else:
        expiry_date = current_time.date()
    
    return expiry_date.strftime('%Y-%m-%d')

def get_btc_options_chain():
    """
    Fetch BTC options chain from Delta Exchange for nearest daily expiry.
    Returns: list - Options data with strikes, premiums, etc.
    """
    try:
        # Get products list
        url = "https://api.delta.exchange/v2/products"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('result', [])
        
        # Get nearest expiry date
        target_expiry = get_nearest_daily_expiry()
        
        # Filter for BTC options with target expiry
        btc_options = []
        for product in products:
            if (product.get('product_type') == 'options' and 
                'BTC' in product.get('symbol', '') and
                product.get('settlement_time', '').startswith(target_expiry)):
                
                # Parse option details
                symbol = product.get('symbol', '')
                
                # Extract strike and option type from symbol
                # Example: BTC-14AUG25-95000-C or BTC-14AUG25-95000-P
                parts = symbol.split('-')
                if len(parts) >= 4:
                    try:
                        strike_price = float(parts[2])
                        option_type = 'call' if parts[3] == 'C' else 'put'
                        
                        option_data = {
                            'symbol': symbol,
                            'product_id': product.get('id'),
                            'strike_price': strike_price,
                            'option_type': option_type,
                            'expiry_date': target_expiry,
                            'mark_price': product.get('mark_price', 0),
                            'last_price': product.get('last_price', 0),
                            'bid_price': product.get('best_bid_price', 0),
                            'ask_price': product.get('best_ask_price', 0),
                            'volume': product.get('volume', 0),
                            'open_interest': product.get('open_interest', 0)
                        }
                        
                        # Convert prices to float
                        for price_field in ['mark_price', 'last_price', 'bid_price', 'ask_price']:
                            if option_data[price_field]:
                                option_data[price_field] = float(option_data[price_field])
                        
                        btc_options.append(option_data)
                        
                    except (ValueError, IndexError):
                        continue  # Skip malformed symbols
        
        # Sort by strike price
        btc_options.sort(key=lambda x: x['strike_price'])
        
        return btc_options
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error fetching options chain: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing options chain: {str(e)}")

def get_option_greeks(product_id):
    """
    Fetch option Greeks for a specific product (if available).
    Returns: dict - Greeks data (delta, gamma, theta, vega, iv)
    """
    try:
        url = f"https://api.delta.exchange/v2/products/{product_id}/greeks"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('result', {})
        else:
            return {}
            
    except Exception:
        return {}

# Test functions
if __name__ == "__main__":
    try:
        print("Testing BTC spot price...")
        price = get_btc_spot_price()
        print(f"Current BTC price: ${price:,.2f}")
        
        print("\nTesting nearest expiry...")
        expiry = get_nearest_daily_expiry()
        print(f"Nearest daily expiry: {expiry}")
        
        print("\nTesting options chain...")
        options = get_btc_options_chain()
        print(f"Found {len(options)} BTC options")
        
        if options:
            print("\nSample options:")
            for i, option in enumerate(options[:5]):
                print(f"{i+1}. {option['symbol']} - Strike: ${option['strike_price']:,.0f} - Premium: ₹{option['mark_price']:.2f}")
    
    except Exception as e:
        print(f"Test failed: {e}")