import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
import io
import openpyxl
from openpyxl.styles import Font, PatternFill

# Page configuration
st.set_page_config(
    page_title="EMA Alignment Scanner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI styling with blue theme
st.markdown("""
<style>
    /* Overall page styling */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #0d4b9f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
    }
    
    h2, h3 {
        color: #334155;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    /* Containers */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
        padding: 2rem 1rem;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 0;
    }
    
    section[data-testid="stSidebar"] h2 {
        margin-top: 0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1e40af;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #1e3a8a;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* DataFrames */
    .dataframe {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .dataframe th {
        background-color: #f1f5f9;
        color: #334155;
        font-weight: 600;
        border: none !important;
        text-align: left !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid #e2e8f0 !important;
        border-left: none !important;
        border-right: none !important;
        text-align: left !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem;
        border: none;
        border-bottom: 2px solid transparent;
        font-weight: 500;
        color: #64748b;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #1e40af !important;
        color: #1e40af !important;
        background-color: transparent !important;
    }
    
    /* Radio buttons */
    div[role="radiogroup"] label {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    div[role="radiogroup"] label:hover {
        border-color: #cbd5e1;
        background-color: #f8fafc;
    }
    
    div[role="radiogroup"] [data-baseweb="radio"] input:checked + div {
        border-color: #2e7d32;
        background-color: #e8f5e9;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        border-radius: 6px !important;
        border-color: #e2e8f0 !important;
        background-color: white;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #cbd5e1 !important;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 6px;
    }
    
    /* Fix for dark mode */
    @media (prefers-color-scheme: dark) {
        .stApp, body, [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
        }
        
        h1, h2, h3, p, span, div {
            color: #f8f9fa;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #f8f9fa;
        }
        
        section[data-testid="stSidebar"] {
            background-color: #262730;
            border-right: 1px solid #4b5563;
        }
        
        .dataframe th {
            background-color: #1e293b;
            color: #f8f9fa;
        }
        
        .dataframe td {
            border-bottom: 1px solid #4b5563 !important;
            color: #f8f9fa;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define stock markets data
us_indices = {
    'S&P 500': '^GSPC',
    'Dow Jones': '^DJI',
    'NASDAQ': '^IXIC'
}

india_indices = {
    'NIFTY 50': '^NSEI',
    'SENSEX': '^BSESN',
    'NIFTY BANK': '^NSEBANK'
}

# Function to load stock lists
@st.cache_data(ttl=86400)
def load_stock_lists():
    # Load US Stocks from CSV
    try:
        us_stocks = pd.read_csv('data/us_stocks.csv')
        if not all(col in us_stocks.columns for col in ['symbol', 'name']):
            us_stocks = us_stocks.rename(columns={
                'Symbol': 'symbol',
                'Company': 'name'
            })
    except Exception as e:
        st.warning(f"Failed to load US stocks CSV: {e}. Using default list.")
        us_stocks = pd.DataFrame({
            'symbol': ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT'],
            'name': ['Apple', 'Microsoft', 'Amazon', 'Alphabet', 'Meta Platforms', 'Tesla', 'NVIDIA', 'JPMorgan Chase', 'Visa', 'Walmart']
        })
    
    # Load Indian Stocks from CSV
    try:
        india_stocks = pd.read_csv('data/india_stocks.csv')
        if not all(col in india_stocks.columns for col in ['symbol', 'name']):
            india_stocks = india_stocks.rename(columns={
                'Symbol': 'symbol',
                'Company': 'name'
            })
        
        # Ensure Indian stock symbols have .NS suffix for API calls
        india_stocks['symbol'] = india_stocks['symbol'].apply(
            lambda x: x if str(x).endswith('.NS') else f"{x}.NS"
        )
    except Exception as e:
        st.warning(f"Failed to load India stocks CSV: {e}. Using default list.")
        india_stocks = pd.DataFrame({
            'symbol': ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 
                     'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS'],
            'name': ['Reliance Industries', 'Tata Consultancy Services', 'HDFC Bank', 'Infosys', 
                    'ICICI Bank', 'Hindustan Unilever', 'ITC', 'State Bank of India', 
                    'Bajaj Finance', 'Bharti Airtel']
        })
    
    return us_stocks, india_stocks

# Function to process uploaded stock list
def process_uploaded_stock_list(uploaded_file, market):
    try:
        # Read Excel or CSV file
        if uploaded_file.name.endswith('.xlsx'):
            stocks_df = pd.read_excel(uploaded_file)
        else:
            content = uploaded_file.read()
            stocks_df = pd.read_csv(io.BytesIO(content))
        
        # Standardize column names (case-insensitive)
        column_mapping = {}
        for col in stocks_df.columns:
            if col.lower() in ['symbol', 'ticker', 'stock']:
                column_mapping[col] = 'symbol'
            elif col.lower() in ['name', 'company', 'company name', 'stock name']:
                column_mapping[col] = 'name'
        
        # Rename columns if needed
        if column_mapping:
            stocks_df = stocks_df.rename(columns=column_mapping)
        
        # Check if we have the required columns
        if 'symbol' not in stocks_df.columns:
            raise ValueError("File must contain a 'symbol' column")
        
        # If no name column exists, create one with symbol values
        if 'name' not in stocks_df.columns:
            stocks_df['name'] = stocks_df['symbol']
        
        # Ensure proper formatting for Indian stocks
        if market == "India":
            stocks_df['symbol'] = stocks_df['symbol'].apply(
                lambda x: x if str(x).endswith('.NS') else f"{x}.NS"
            )
        
        # Limit to 9999 stocks
        if len(stocks_df) > 9999:
            stocks_df = stocks_df.iloc[:9999]
            st.warning(f"Stock list limited to 9999 stocks")
        
        return stocks_df
        
    except Exception as e:
        st.error(f"Error processing uploaded file: {e}")
        return None

# Function to get stock data and calculate EMAs
@st.cache_data(ttl=3600)
def get_stock_data(symbol, timeframe):
    try:
        stock = yf.Ticker(symbol)
        
        # Set period based on timeframe
        if timeframe == "1d":
            period = "500d"
        else:  # 1h
            period = "90d"
            
        df = stock.history(period=period, interval=timeframe)
        
        if df.empty or len(df) < 200:  # Ensure we have enough data for EMAs
            return None
        
        # Calculate EMAs precisely
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()
        df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        return df
    except Exception as e:
        return None

# Function to check EMA alignment
def check_ema_alignment(df):
    if df is None or df.empty:
        return None, None
    
    # Get the latest values
    latest = df.iloc[-1]
    close_price = latest['Close']
    ema20 = latest['EMA20']
    ema50 = latest['EMA50']
    ema100 = latest['EMA100']
    ema200 = latest['EMA200']
    
    # Check bullish alignment: Close > EMA20 > EMA50 > EMA100 > EMA200
    is_bullish = (close_price > ema20 > ema50 > ema100 > ema200)
    
    # Check bearish alignment: Close < EMA20 < EMA50 < EMA100 < EMA200
    is_bearish = (close_price < ema20 < ema50 < ema100 < ema200)
    
    if is_bullish:
        return "Bullish", "🟢"
    elif is_bearish:
        return "Bearish", "🔴"
    else:
        return None, None

# Function to scan all stocks for EMA alignment
def scan_ema_alignment(stock_list, timeframe, market):
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_stocks = len(stock_list)
    processed_count = 0
    
    for i, (symbol, name) in enumerate(zip(stock_list['symbol'], stock_list['name'])):
        status_text.text(f"Scanning {market} stocks: {i+1}/{total_stocks} - {name} ({symbol})")
        progress_bar.progress((i + 1) / total_stocks)
        
        df = get_stock_data(symbol, timeframe)
        
        if df is None or df.empty:
            continue
            
        processed_count += 1
        
        trend, status_emoji = check_ema_alignment(df)
        
        if trend:  # Only add if bullish or bearish alignment found
            # Remove .NS suffix for display
            display_symbol = symbol.replace('.NS', '') if symbol.endswith('.NS') else symbol
            
            results.append({
                'Symbol': display_symbol,
                'Company Name': name,
                'Trend': trend,
                'Status': status_emoji,
                'Original_Symbol': symbol  # Keep original for any further processing
            })
    
    progress_bar.empty()
    status_text.empty()
    
    # Show summary of scan results
    if processed_count < total_stocks:
        st.info(f"Note: Data for {total_stocks - processed_count} stocks could not be retrieved or processed.")
    
    return pd.DataFrame(results) if results else pd.DataFrame()

# Function to create formatted Excel file
def create_formatted_excel(df, filename):
    if df.empty:
        return None
    
    # Create a copy of dataframe for export (without Original_Symbol)
    export_df = df[['Symbol', 'Company Name', 'Trend', 'Status']].copy()
    
    # Create Excel file in memory
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, sheet_name='EMA Alignment Results', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['EMA Alignment Results']
        
        # Define colors
        green_font = Font(color="00008000", bold=True)  # Green
        red_font = Font(color="00FF0000", bold=True)    # Red
        
        # Format the data rows
        for row in range(2, len(export_df) + 2):  # Start from row 2, skip header
            trend_value = worksheet[f'C{row}'].value
            if trend_value == 'Bullish':
                # Color the entire row green for bullish stocks
                for col in ['A', 'B', 'C', 'D']:
                    worksheet[f'{col}{row}'].font = green_font
            elif trend_value == 'Bearish':
                # Color the entire row red for bearish stocks
                for col in ['A', 'B', 'C', 'D']:
                    worksheet[f'{col}{row}'].font = red_font
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    return output

# Main application
def main():
    st.title("EMA Alignment Scanner")
    
    # Display current market status at the top
    st.subheader("Market Status")
    col1, col2, col3 = st.columns(3)
    
    # Initialize session state for managing stock lists
    if 'using_custom_list' not in st.session_state:
        st.session_state.using_custom_list = False
    
    # Sidebar
    st.sidebar.header("Scanner Settings")
    
    # Load default stock lists
    us_stocks, india_stocks = load_stock_lists()
    
    # Custom stock list upload
    st.sidebar.subheader("Stock List")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Custom (Symbol, Name)",
        type=["csv", "xlsx"],
        help="CSV or Excel file with 'symbol' and 'name' columns (Max 50MB, 9999 stocks)"
    )
    
    # Process uploaded file if available
    custom_stocks = None
    if uploaded_file is not None:
        if uploaded_file.size > 50 * 1024 * 1024:  # 50MB limit
            st.sidebar.error("File size exceeds 50MB limit")
            st.session_state.using_custom_list = False
        else:
            market_for_processing = st.session_state.get('market', "US")
            custom_stocks = process_uploaded_stock_list(uploaded_file, market_for_processing)
            
            if custom_stocks is not None:
                st.session_state.using_custom_list = True
                st.session_state.custom_stocks = custom_stocks
                st.sidebar.success(f"Loaded {len(custom_stocks)} stocks from your file")
            else:
                st.session_state.using_custom_list = False
    else:
        st.session_state.using_custom_list = False
    
    # Market selection
    if st.session_state.using_custom_list:
        market = st.sidebar.selectbox(
            "Select Market (Disabled - Using Custom List)",
            ["US", "India"],
            disabled=True,
            index=0 if st.session_state.get('market') == "US" else 1
        )
        market = st.session_state.get('market', "US")
    else:
        market = st.sidebar.selectbox("Select Market", ["US", "India"])
        st.session_state.market = market
    
    # Timeframe selection - only Daily and Hourly
    timeframe_options = {
        "Daily": "1d",
        "Hourly": "1h"
    }
    timeframe_display = st.sidebar.selectbox("Select Timeframe", list(timeframe_options.keys()))
    timeframe = timeframe_options[timeframe_display]
    
    # Scan button
    scan_button = st.sidebar.button("Start EMA Alignment Scan", use_container_width=True)
    
    # Display current market status data
    indices = us_indices if market == "US" else india_indices
    
    index_cols = [col1, col2, col3]
    for i, (index_name, index_symbol) in enumerate(indices.items()):
        try:
            index_data = yf.Ticker(index_symbol).history(period="1d")
            if not index_data.empty:
                current = index_data['Close'].iloc[-1]
                previous = index_data['Open'].iloc[-1]
                change = current - previous
                change_percent = (change / previous) * 100
                
                color = "green" if change >= 0 else "red"
                change_icon = "▲" if change >= 0 else "▼"
                
                index_cols[i].markdown(
                    f"**{index_name}**: {current:.2f} "
                    f"<span style='color:{color}'>{change_icon} {abs(change):.2f} ({abs(change_percent):.2f}%)</span>", 
                    unsafe_allow_html=True
                )
        except:
            index_cols[i].text(f"{index_name}: Data unavailable")
    
    if scan_button:
        # Use custom stock list if uploaded, otherwise use default
        if st.session_state.using_custom_list:
            stocks_to_scan = st.session_state.custom_stocks
        else:
            stocks_to_scan = us_stocks if market == "US" else india_stocks
        
        with st.spinner(f"Scanning {market} stocks for EMA alignment on {timeframe_display} timeframe..."):
            results_df = scan_ema_alignment(stocks_to_scan, timeframe, market)
        
        # Store results in session state
        st.session_state.results_df = results_df
        st.session_state.last_scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.market = market
        st.session_state.timeframe = timeframe_display
    
    # Display explanation
    with st.expander("How This EMA Alignment Scanner Works"):
        st.markdown(f"""
        **Disclaimer**: This project is intended for educational and informational purposes only. You are solely responsible for any profits or losses you may incur.
        
        ## EMA Alignment Scanner Logic
        
        This scanner identifies stocks with perfect EMA alignment:
        
        ### 🟢 Bullish Stocks
        - Latest Close Price > EMA 20 > EMA 50 > EMA 100 > EMA 200
        - Perfect bullish alignment indicates strong upward momentum
        
        ### 🔴 Bearish Stocks  
        - Latest Close Price < EMA 20 < EMA 50 < EMA 100 < EMA 200
        - Perfect bearish alignment indicates strong downward momentum
        
        ### Timeframes Available
        - **Daily**: Uses 500 days of data for precise EMA calculations
        - **Hourly**: Uses 90 days of data for intraday analysis
        
        ### Important Notes
        - All EMAs are calculated precisely using exponential weighting
        - Only stocks with perfect alignment are shown
        - Indian stock symbols display without .NS suffix in results
        - Export files are formatted with color coding (Green for Bullish, Red for Bearish)
        
        ### Using Custom Stock Lists
        - Upload CSV or Excel files with 'symbol' and 'name' columns
        - Maximum 9999 stocks per list and 50MB file size
        - For Indian stocks, .NS suffix is automatically handled
        """)
    
    # Display results
    if 'results_df' in st.session_state and not st.session_state.results_df.empty:
        st.subheader("EMA Alignment Results")
        
        # Show last scan info
        scan_info = f"Last scan: {st.session_state.last_scan_time} | Market: {st.session_state.market} | Timeframe: {st.session_state.timeframe}"
        st.info(scan_info)
        
        # Separate bullish and bearish stocks
        bullish_stocks = st.session_state.results_df[st.session_state.results_df['Trend'] == 'Bullish']
        bearish_stocks = st.session_state.results_df[st.session_state.results_df['Trend'] == 'Bearish']
        
        # Create tabs for bullish and bearish
        tab1, tab2 = st.tabs([f"Bullish Stocks 🟢 ({len(bullish_stocks)})", f"Bearish Stocks 🔴 ({len(bearish_stocks)})"])
        
        with tab1:
            if not bullish_stocks.empty:
                st.subheader("Perfect Bullish EMA Alignment")
                display_df = bullish_stocks[['Symbol', 'Company Name', 'Trend', 'Status']].copy()
                st.dataframe(display_df, use_container_width=True)
                
                # Download button for bullish stocks
                excel_file = create_formatted_excel(bullish_stocks, f"bullish_stocks_{st.session_state.market}_{st.session_state.timeframe}")
                if excel_file:
                    st.download_button(
                        label="📥 Download Bullish Stocks (Excel)",
                        data=excel_file.getvalue(),
                        file_name=f"bullish_stocks_{st.session_state.market}_{st.session_state.timeframe}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("No stocks found with perfect bullish EMA alignment.")
        
        with tab2:
            if not bearish_stocks.empty:
                st.subheader("Perfect Bearish EMA Alignment")
                display_df = bearish_stocks[['Symbol', 'Company Name', 'Trend', 'Status']].copy()
                st.dataframe(display_df, use_container_width=True)
                
                # Download button for bearish stocks
                excel_file = create_formatted_excel(bearish_stocks, f"bearish_stocks_{st.session_state.market}_{st.session_state.timeframe}")
                if excel_file:
                    st.download_button(
                        label="📥 Download Bearish Stocks (Excel)",
                        data=excel_file.getvalue(),
                        file_name=f"bearish_stocks_{st.session_state.market}_{st.session_state.timeframe}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("No stocks found with perfect bearish EMA alignment.")
        
        # Download all results button
        if not st.session_state.results_df.empty:
            st.subheader("Download All Results")
            excel_file = create_formatted_excel(st.session_state.results_df, f"ema_alignment_results_{st.session_state.market}_{st.session_state.timeframe}")
            if excel_file:
                st.download_button(
                    label="📥 Download All Results (Excel)",
                    data=excel_file.getvalue(),
                    file_name=f"ema_alignment_results_{st.session_state.market}_{st.session_state.timeframe}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    elif 'last_scan_time' in st.session_state:
        st.info("No stocks found with perfect EMA alignment. Try scanning with different parameters.")
    else:
        st.info("Click 'Start EMA Alignment Scan' to begin scanning for stocks with perfect EMA alignment.")

# Run the application
if __name__ == "__main__":
    main()