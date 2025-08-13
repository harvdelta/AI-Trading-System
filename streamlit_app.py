import streamlit as st
import json
from datetime import datetime
import pytz
from logic.logic1 import logic1

# Configure Streamlit page
st.set_page_config(
    page_title="BTC Options Alert System",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("₿ BTC Options Alert System (Dry Run)")
    st.markdown("---")
    
    # Create columns for layout
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.header("📊 Current Status")
        
        # Auto-refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            st.rerun()
    
    with col2:
        st.header("⏰ System Time")
        ist_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist_tz)
        st.info(f"Current IST: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col3:
        st.header("💾 Cache")
        try:
            with open('price_cache.json', 'r') as f:
                cache_data = json.load(f)
            st.success("Cache loaded")
        except FileNotFoundError:
            cache_data = {"status": "No cache file"}
            st.warning("No cache file")
    
    st.markdown("---")
    
    # Main logic execution
    try:
        result = logic1()
        
        # Display main result
        st.header("🎯 Trading Logic Result")
        
        if result.get('status') == 'ALERT':
            if result.get('direction') == 'UP':
                st.success(f"🚀 **BULLISH ALERT**: {result.get('message', '')}")
            elif result.get('direction') == 'DOWN':
                st.error(f"🐻 **BEARISH ALERT**: {result.get('message', '')}")
        elif result.get('status') == 'NO_TRIGGER':
            st.info(f"😴 **NO TRIGGER**: {result.get('message', '')}")
        elif result.get('status') == 'WAITING':
            st.warning(f"⏳ **WAITING**: {result.get('message', '')}")
        else:
            st.info(f"ℹ️ **STATUS**: {result.get('message', '')}")
        
        # Detailed information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Price Information")
            if 'current_price' in result:
                st.metric("Current BTC Price", f"${result['current_price']:,.2f}")
            if 'am_open' in result:
                st.metric("AM Open Price", f"${result['am_open']:,.2f}")
            if 'move_percent' in result:
                st.metric("Movement %", f"{result['move_percent']:.2f}%", 
                         delta=f"{result['move_percent']:.2f}%")
        
        with col2:
            st.subheader("⚙️ System Details")
            st.json(result, expanded=False)
        
        # Options chain information (if available)
        if 'selected_option' in result:
            st.subheader("🎯 Selected Options")
            st.json(result['selected_option'])
        
    except Exception as e:
        st.error(f"❌ Error executing logic: {str(e)}")
        st.exception(e)
    
    # Cache information
    st.markdown("---")
    st.subheader("💾 Price Cache Status")
    
    try:
        with open('price_cache.json', 'r') as f:
            cache_data = json.load(f)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            am_price = cache_data.get('am_open', 'Not set')
            if isinstance(am_price, (int, float)):
                st.metric("AM Open (5:29:59 AM)", f"${am_price:,.2f}")
            else:
                st.metric("AM Open (5:29:59 AM)", am_price)
        
        with col2:
            pm_price = cache_data.get('pm_open', 'Not set')
            if isinstance(pm_price, (int, float)):
                st.metric("PM Open (5:29:59 PM)", f"${pm_price:,.2f}")
            else:
                st.metric("PM Open (5:29:59 PM)", pm_price)
        
        with col3:
            last_update = cache_data.get('last_update_date', 'Never')
            st.metric("Last Update", last_update)
        
        # Raw cache data
        with st.expander("Raw Cache Data"):
            st.json(cache_data)
    
    except FileNotFoundError:
        st.warning("No price cache file found. It will be created automatically.")
    except Exception as e:
        st.error(f"Error reading cache: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("**⚠️ Dry Run Mode**: No real trades will be executed. This is for testing only.")

if __name__ == "__main__":
    main()
