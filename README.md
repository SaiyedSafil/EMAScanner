# EMA Alignment Scanner 📈

A powerful Streamlit web application that scans stocks for perfect EMA (Exponential Moving Average) alignment patterns to identify strong trending opportunities in both Indian and US markets.

## 🚀 Features

### Core Functionality
- **Perfect EMA Alignment Detection**: Identifies stocks with precise bullish or bearish EMA alignment
- **Multi-Market Support**: Scan both Indian (NSE) and US stock markets
- **Multiple Timeframes**: Daily, Hourly, and Weekly analysis
- **Custom Stock Lists**: Upload your own Excel files with stock symbols
- **Real-time Market Status**: Live index data display
- **Export Results**: Download results in formatted Excel files with color coding

### EMA Alignment Logic
- **Bullish Alignment**: Close Price > EMA20 > EMA50 > EMA100 > EMA200
- **Bearish Alignment**: Close Price < EMA20 < EMA50 < EMA100 < EMA200

## 📋 Requirements

```
streamlit
yfinance
pandas
numpy
openpyxl
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ema-alignment-scanner.git
cd ema-alignment-scanner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create data directory and stock files**
```bash
mkdir data
```

4. **Add stock data files** (Optional - app includes defaults)
   - `data/us_stocks.xlsx` - US stocks with columns: Symbol, Company Name
   - `data/india_stocks.xlsx` - Indian stocks with columns: Symbol, Company Name

## 🚀 Usage

1. **Run the application**
```bash
streamlit run app.py
```

2. **Access the web interface**
   - Open your browser to `http://localhost:8501`

3. **Configure scan settings**
   - Select market (India/US)
   - Choose timeframe (Daily/Hourly/Weekly)
   - Optionally upload custom stock list

4. **Start scanning**
   - Click "Start EMA Alignment Scan"
   - View results in Bullish/Bearish tabs
   - Download formatted Excel reports

## 📊 Timeframe Details

| Timeframe | Data Period | Use Case |
|-----------|-------------|----------|
| **Daily** | 500 days | Mid-term trend analysis |
| **Hourly** | 90 days | Swing trading opportunities |
| **Weekly** | 7 years | Long-term investment trends |

## 📁 File Structure

```
ema-alignment-scanner/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Stock data directory
│   ├── us_stocks.xlsx    # US stock symbols (optional)
│   └── india_stocks.xlsx # Indian stock symbols (optional)
└── .gitignore           # Git ignore file
```

## 📈 Default Stock Coverage

### Indian Market
- **Indices**: NIFTY 50, SENSEX, NIFTY BANK
- **Default Stocks**: Top 10 NSE stocks including Reliance, TCS, HDFC Bank, etc.

### US Market  
- **Indices**: S&P 500, Dow Jones, NASDAQ
- **Default Stocks**: Top 10 US stocks including AAPL, MSFT, AMZN, etc.

## 📤 Custom Stock Lists

### Upload Format
- **File Type**: Excel (.xlsx) only
- **Required Columns**: 
  - `Symbol` - Stock ticker symbol
  - `Company Name` - Full company name
- **Limits**: 
  - Maximum 9,999 stocks per file
  - Maximum file size: 50MB

### Symbol Format
- **US Stocks**: Use standard ticker symbols (e.g., AAPL, MSFT)
- **Indian Stocks**: App automatically adds .NS suffix (e.g., RELIANCE becomes RELIANCE.NS)
- **Indices**: Use ^ prefix (e.g., ^NSEI, ^GSPC)

## 🎨 Features & UI

### Modern Interface
- Clean, professional blue-themed design
- Responsive layout with sidebar controls
- Real-time progress indicators during scans
- Tabbed results view (Bullish/Bearish)

### Export Capabilities
- **Individual Downloads**: Separate files for bullish and bearish stocks
- **Combined Export**: All results in single file
- **Excel Formatting**: Color-coded cells (Green for bullish, Red for bearish)
- **Auto-sizing**: Columns automatically adjust to content

## ⚠️ Important Notes

### Security Features
- Input sanitization for all stock symbols and company names
- Protection against injection attacks
- File size and content validation

### Data Limitations
- **API Dependency**: Uses Yahoo Finance API (yfinance)
- **Rate Limiting**: Large scans may take time due to API limits
- **Data Availability**: Some stocks may not have sufficient historical data
- **Market Hours**: Real-time data depends on market operating hours

### Disclaimers
- **Educational Purpose**: This tool is for educational and informational use only
- **Investment Risk**: Users are solely responsible for any trading decisions and outcomes
- **No Financial Advice**: Results should not be considered as investment recommendations

## 🔧 Troubleshooting

### Common Issues

1. **Stocks not loading**
   - Check internet connection
   - Verify stock symbols are correct
   - Ensure sufficient historical data exists

2. **Custom file upload fails**
   - Verify Excel format (.xlsx)
   - Check column names (Symbol, Company Name)
   - Ensure file size under 50MB

3. **Slow scanning**
   - Large stock lists take time
   - Consider reducing timeframe data requirements
   - Check network stability

### Performance Tips
- Use smaller stock lists for faster results
- Daily timeframe provides good balance of speed and accuracy
- Upload custom lists with verified, active stock symbols

## 📊 Sample Output

The scanner provides:
- **Summary Statistics**: Count of bullish vs bearish stocks
- **Detailed Results**: Symbol, company name, and trend direction
- **Market Context**: Current index values and changes
- **Export Options**: Formatted Excel files with color coding

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **yfinance**: Yahoo Finance API wrapper
- **Streamlit**: Web application framework
- **OpenPyXL**: Excel file processing
- **Pandas/NumPy**: Data manipulation and analysis

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**⚠️ Risk Warning**: Trading and investing in stocks involves substantial risk of loss. Past performance does not guarantee future results. Always conduct your own research and consider consulting with a financial advisor before making investment decisions.
