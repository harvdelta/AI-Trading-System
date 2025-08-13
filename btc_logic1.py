import json
import os
from datetime import datetime
import pytz
from .data_fetch import get_btc_spot_price, get_btc_options_chain

def update_price_cache():
    """Update the price cache with AM/PM prices at specific times."""
    
    # Get current IST time
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_tz)
    current_date = current_time.strftime('%Y-%m-%d')
    current_time_str = current_time.strftime('%H:%M:%S')
    
    # Load existing cache or create new one
    cache_file = 'price_cache.json'
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {
            'am_open': None,
            'pm_open': None,
            'last_update_date': None
        }
    
    # Check if we need to reset for a new day
    if cache.get('last_update_date') != current_date:
        cache['am_open'] = None
        cache['pm_open'] = None
    
    updated = False
    
    # Check for AM price capture (5:29:59 AM IST)
    if current_time_str == '05:29:59':
        try:
            btc_price = get_btc_spot_price()
            cache['am_open'] = btc_price
            cache['last_update_date'] = current_date
            updated = True
            print(f"AM price captured: ${btc_price:,.2f}")
        except Exception as e:
            print(f"Error capturing AM price: {e}")
    
    # Check for PM price capture (5:29:59 PM IST)
    elif current_time_str == '17:29:59':
        try:
            btc_price = get_btc_spot_price()
            cache['pm_open'] = btc_price
            cache['last_update_date'] = current_date
            updated = True
            print(f"PM price captured: ${btc_price:,.2f}")
        except Exception as e:
            print(f"Error capturing PM price: {e}")
    
    # Save cache if updated
    if updated:
        with open(cache_file, 'w') as f:
            json.dump(cache, f, indent=2)
    
    return cache

def find_target_option(options_chain, option_type, target_premium, current_btc_price):
    """Find OTM option closest to target premium."""
    
    if not options_chain:
        return None
    
    best_option = None
    best_diff = float('inf')
    
    for option in options_chain:
        # Check if it's the right type
        if option.get('option_type', '').lower() != option_type.lower():
            continue
        
        # Check if it's OTM
        strike = option.get('strike_price', 0)
        if option_type.lower() == 'call' and strike <= current_btc_price:
            continue  # Call must be above current price
        if option_type.lower() == 'put' and strike >= current_btc_price:
            continue  # Put must be below current price
        
        # Check premium
        premium = option.get('mark_price', option.get('last_price', 0))
        if premium <= 0:
            continue
        
        # Calculate difference from target
        premium_diff = abs(premium - target_premium)
        
        if premium_diff < best_diff:
            best_diff = premium_diff
            best_option = option
    
    return best_option

def logic1():
    """
    Main trading logic:
    1. Update price cache for AM/PM prices
    2. Check if BTC moved ±1.5% from AM open
    3. If yes, select appropriate options and return alert
    """
    
    try:
        # Update price cache
        cache = update_price_cache()
        
        # Get current IST time
        ist_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist_tz)
        current_date = current_time.strftime('%Y-%m-%d')
        
        # Check if AM price is available for today
        if not cache.get('am_open') or cache.get('last_update_date') != current_date:
            return {
                'status': 'WAITING',
                'message': 'Waiting for AM open price (5:29:59 AM IST)',
                'current_time': current_time.strftime('%H:%M:%S IST'),
                'cache_date': cache.get('last_update_date'),
                'current_date': current_date
            }
        
        # Get current BTC price
        try:
            current_price = get_btc_spot_price()
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Failed to fetch current BTC price: {str(e)}'
            }
        
        # Calculate movement from AM open
        am_open = cache['am_open']
        move_percent = ((current_price - am_open) / am_open) * 100
        
        result = {
            'status': 'NO_TRIGGER',
            'current_price': current_price,
            'am_open': am_open,
            'move_percent': move_percent,
            'current_time': current_time.strftime('%H:%M:%S IST'),
            'message': f'Movement: {move_percent:.2f}% (Need ±1.5% for trigger)'
        }
        
        # Check for trigger conditions
        if move_percent >= 1.5:
            # Bullish move - find OTM call near ₹200 premium
            try:
                options_chain = get_btc_options_chain()
                target_call = find_target_option(options_chain, 'call', 200, current_price)
                
                result.update({
                    'status': 'ALERT',
                    'direction': 'UP',
                    'message': f'BTC up {move_percent:.2f}% - SELL OTM CALL (Target: 20 lots)',
                    'target_premium': 200,
                    'target_lots': 20,
                    'selected_option': target_call
                })
            except Exception as e:
                result.update({
                    'status': 'ALERT',
                    'direction': 'UP',
                    'message': f'BTC up {move_percent:.2f}% - Options selection failed: {str(e)}',
                    'target_premium': 200,
                    'target_lots': 20
                })
        
        elif move_percent <= -1.5:
            # Bearish move - find OTM put near ₹100 premium
            try:
                options_chain = get_btc_options_chain()
                target_put = find_target_option(options_chain, 'put', 100, current_price)
                
                result.update({
                    'status': 'ALERT',
                    'direction': 'DOWN',
                    'message': f'BTC down {move_percent:.2f}% - SELL OTM PUT (Target: 15 lots)',
                    'target_premium': 100,
                    'target_lots': 15,
                    'selected_option': target_put
                })
            except Exception as e:
                result.update({
                    'status': 'ALERT',
                    'direction': 'DOWN',
                    'message': f'BTC down {move_percent:.2f}% - Options selection failed: {str(e)}',
                    'target_premium': 100,
                    'target_lots': 15
                })
        
        return result
    
    except Exception as e:
        return {
            'status': 'ERROR',
            'message': f'System error: {str(e)}',
            'error_type': type(e).__name__
        }