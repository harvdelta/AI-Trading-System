# ₿ BTC Options Alert System

A comprehensive automated trading alert system for Bitcoin options on Delta Exchange. The system monitors BTC price movements and generates alerts when specific conditions are met.

## 🎯 Features

- **Automatic Price Tracking**: Captures BTC prices at 5:29:59 AM and PM IST daily
- **Movement Detection**: Alerts when BTC moves ±1.5% from AM open price
- **Options Selection**: Automatically finds optimal OTM options with target premiums
- **Dry Run Mode**: Safe testing without real trades
- **Streamlit Web Interface**: Real-time monitoring dashboard
- **Cloud Ready**: Deploys easily on Streamlit Cloud

## 📊 Trading Logic

### Logic 1: Momentum-Based Options Selling

**Trigger Conditions:**
- **Bullish Alert** (≥+1.5% from AM open):
  - Find OTM call option near ₹200 premium
  - Recommended action: Sell 20 lots
- **Bearish Alert** (≤-1.5% from AM open):
  - Find OTM put option near ₹100 premium  
  - Recommended action: Sell 15 lots

**Timing:**
- AM price captured at exactly 5:29:59 AM IST
- PM price captured at exactly 5:29:59 PM IST
- Continuous monitoring during market hours

## 🏗️ System Architecture

```
btc-options-alert/
├── streamlit_app.py          # Main Streamlit interface
├── logic/
│   ├── __init__.py
│   ├── logic1.py             # Core trading logic
│   └── data_fetch.py         # Delta Exchange API integration
├── price_cache.json          # Automated price storage
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone and setup:**
```bash
git clone <your-repo>
cd btc-options-alert
pip install -r requirements.txt
```

2. **Run the application:**
```bash
streamlit run streamlit_app.py
```

3. **Access dashboard:**
- Open browser to `http://localhost:8501`
- Click "Refresh Data" to run logic checks

### Streamlit Cloud Deployment

1. **Push to GitHub:**
```bash
git add .
git commit -m "Deploy BTC options alert system"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub repo
- Set main file: `streamlit_app.py`
- Deploy!

## 📱 Web Interface Features

### Dashboard Sections

**📊 Current Status**
- Real-time trading alerts
- Movement percentage display
- Current vs AM open price comparison

**⏰ System Time**
- Current IST timestamp
- Price capture timing status

**💾 Price Cache**
- AM/PM price history
- Last update timestamps
- Cache data visualization

**🎯 Options Selection**
- Selected strike prices
- Premium information
- Trading recommendations

## 🔧 Configuration

### Price Cache (`price_cache.json`)
```json
{
  "am_open": 65432.50,
  "pm_open": 66120.75,
  "last_update_date": "2025-08-14"
}
```

**Automatic Updates:**
- File created automatically on first run
- AM price: captured at 5:29:59 AM IST
- PM price: captured at 5:29:59 PM IST
- Resets daily for new trading sessions

### API Configuration

**Delta Exchange Endpoints:**
- Spot prices: `/v2/products`
- Options chain: `/v2/products` (filtered)
- No authentication required for public data

## 📈 Data Sources

### BTC Spot Price
- **Source**: Delta Exchange BTCUSDT spot
- **Update**: Real-time on each refresh
- **Fallback**: Alternative BTC/USDT pairs

### Options Chain
- **Source**: Delta Exchange BTC options
- **Expiry**: Nearest daily expiry (auto-detected)
- **Data**: Strike prices, premiums, volume, OI

### Price History
- **Storage**: Local JSON file (`price_cache.json`)
- **Retention**: Daily AM/PM prices only
- **Reset**: Automatic daily refresh

## ⚠️ Safety Features

### Dry Run Mode
- **No Real Trades**: All alerts are informational only
- **Safe Testing**: Test logic without financial risk
- **Clear Labeling**: UI clearly shows dry run status

### Error Handling
- **API Failures**: Graceful degradation with error messages
- **Data Validation**: Checks for malformed responses
- **Timeout Protection**: Network request timeouts

### Data Validation
- **Price Sanity Checks**: Validates reasonable BTC price ranges
- **Option Filtering**: Ensures OTM selection logic
- **Cache Integrity**: Validates stored price data

## 🔮 Future Enhancements

### Additional Trading Logic
- Multiple timeframe analysis
- Volume-based triggers
- Volatility-based position sizing

### Advanced Options Features
- Greeks-based selection
- Implied volatility analysis
- Multi-leg strategies

### Risk Management
- Position size optimization
- Stop-loss integration
- Portfolio-level risk metrics

### Notifications
- Email alerts
- Telegram/WhatsApp integration
- Mobile push notifications

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web interface framework
- **Requests**: HTTP API communication
- **PyTZ**: Timezone handling for IST

### Performance
- **Startup**: < 2 seconds
- **API Calls**: < 1 second response time
- **Memory**: < 50MB usage
- **Storage**: < 1KB cache file

### Compatibility
- **Python**: 3.8+
- **Browsers**: Chrome, Firefox, Safari, Edge
- **Mobile**: Responsive design

## 📞 Support

### Common Issues

**"Waiting for AM open price"**
- System needs to capture AM price at 5:29:59 AM IST
- Will auto-resolve next morning

**"Failed to fetch BTC price"**
- Check internet connection
- Delta Exchange API may be down
- Try refreshing after a few minutes

**Empty options chain**
- May occur on weekends/holidays
- Options may not be available for current expiry

### Troubleshooting
1. Check `price_cache.json` exists and has valid data
2. Verify system time is correct (IST timezone)
3. Test API connectivity with manual refresh
4. Check browser console for JavaScript errors

## 📄 License

This project is for educational and testing purposes only. Not financial advice.

**Disclaimer:** Always conduct thorough testing before using any automated trading system with real money. Past performance does not guarantee future results.

---

**Ready to monitor BTC options like a pro? 🚀**

Deploy on Streamlit Cloud and start tracking those momentum moves!
