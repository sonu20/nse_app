import streamlit as st
import pandas as pd
from nselib.libutil import *
from nselib.constants import *
from datetime import datetime
import datetime as dt

st.set_page_config(layout="wide")

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns',300)
pd.set_option('display.width', 300)

@st.cache_data(ttl=300)
def future_oi_eod_data(symbol, startdate, enddate):
    # Ensure dates are in dd-mm-yyyy format for the URL
    
    # Check if the symbol is an index
    indices = ["NIFTY", "BANKNIFTY"]
    
    if symbol in indices:
        instrument_type = "FUTIDX"
    else:
        instrument_type = "FUTSTK"
        
    url = f'https://www.nseindia.com/api/NextApi/apiClient/GetQuoteApi?functionName=getDerivativesHistoricalData&symbol={symbol}&instrumentType={instrument_type}&year=&expiryDate=&strikePrice=&optionType=&fromDate={startdate}&toDate={enddate}'
    
    try:
        data = nse_urlfetch(url).json()
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

# --- Streamlit Sidebar Inputs ---
st.title("NSE Future OI Data Analysis")

with st.sidebar:
    st.header("Configuration")  
    
    # Symbol Selection
    # You can expand this list or fetch it dynamically if needed
    #symbol_list = ['NIFTY','BANKNIFTY','ASHOKLEY', 'AXISBANK', 'BANKINDIA', 'COALINDIA', 'HCLTECH', 'INFY','NESTLEIND', 'LUPIN', 'MCX', 'SBIN', 'TATASTEEL', 'TCS']
    symbol_list = ['NIFTY','BANKNIFTY','360ONE', 'ABB', 'ABCAPITAL', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ALKEM', 'AMBER', 'AMBUJACEM', 'ANGELONE', 'APLAPOLLO', 'APOLLOHOSP', 'ASHOKLEY', 'ASIANPAINT', 'ASTRAL','AUBANK', 'AUROPHARMA', 'AXISBANK', 'BAJAJFINSV', 'BAJAJHLDNG', 'BAJFINANCE', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'BDL', 'BEL', 'BHARATFORG', 'BHARTIARTL', 'BHEL', 'BIOCON', 'BLUESTARCO', 'BOSCHLTD', 'BPCL', 'BRITANNIA', 'BSE', 'CAMS', 'CANBK', 'CDSL', 'CGPOWER', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COFORGE', 'COLPAL', 'CONCOR', 'CROMPTON', 'CUMMINSIND', 'DABUR', 'DALBHARAT', 'DELHIVERY', 'DIVISLAB', 'DIXON', 'DLF', 'DMART', 'DRREDDY', 'EICHERMOT', 'ETERNAL', 'EXIDEIND', 'FEDERALBNK', 'FORTIS', 'GAIL', 'GLENMARK', 'GMRAIRPORT', 'GODREJCP', 'GODREJPROP', 'GRASIM', 'HAL', 'HAVELLS', 'HCLTECH', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HUDCO', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'IDEA', 'IDFCFIRSTB', 'IEX',  'INDHOTEL', 'INDIANB', 'INDIGO', 'INDUSINDBK', 'INDUSTOWER', 'INFY', 'INOXWIND', 'IOC','IREDA', 'IRFC', 'ITC', 'JINDALSTEL', 'JIOFIN', 'JSWENERGY', 'JSWSTEEL', 'JUBLFOOD', 'KALYANKJIL', 'KAYNES', 'KEI', 'KFINTECH', 'KOTAKBANK', 'KPITTECH','LAURUSLABS', 'LICHSGFIN', 'LICI', 'LODHA', 'LT', 'LTF', 'LTIM', 'LUPIN', 'MANAPPURAM', 'MANKIND', 'MARICO', 'MARUTI', 'MAXHEALTH', 'MAZDOCK', 'MCX', 'MFSL', 'MOTHERSON', 'MPHASIS', 'MUTHOOTFIN', 'NATIONALUM', 'NAUKRI', 'NBCC', 'NESTLEIND', 'NHPC', 'NMDC', 'NTPC', 'NUVAMA', 'NYKAA', 'OBEROIRLTY', 'OFSS', 'OIL', 'ONGC', 'PAGEIND', 'PATANJALI', 'PAYTM', 'PERSISTENT', 'PETRONET', 'PFC', 'PGEL', 'PHOENIXLTD', 'PIDILITIND', 'PIIND', 'PNB', 'PNBHOUSING', 'POLICYBZR', 'POLYCAB', 'POWERGRID', 'POWERINDIA', 'PPLPHARMA', 'PREMIERENE', 'PRESTIGE', 'RBLBANK', 'RECLTD', 'RELIANCE', 'RVNL', 'SAIL', 'SAMMAANCAP', 'SBICARD', 'SBILIFE', 'SBIN', 'SHREECEM', 'SHRIRAMFIN', 'SIEMENS', 'SOLARINDS', 'SONACOMS', 'SRF', 'SUNPHARMA', 'SUPREMEIND', 'SUZLON', 'SWIGGY', 'SYNGENE', 'TATACONSUM', 'TATAELXSI', 'TATAPOWER', 'TATASTEEL', 'TATATECH', 'TCS', 'TECHM', 'TIINDIA', 'TITAN', 'TMPV', 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TVSMOTOR', 'ULTRACEMCO', 'UNIONBANK', 'UNITDSPR', 'UNOMINDA', 'UPL', 'VBL', 'VEDL', 'VOLTAS', 'WAAREEENER', 'WIPRO', 'YESBANK', 'ZYDUSLIFE']


    selected_symbol = st.selectbox("Select Symbol", symbol_list, index=symbol_list.index('NIFTY') if 'NIFTY' in symbol_list else 0)

    # Date Range
    st.subheader("Date Range")
    default_start = dt.date(2026, 1, 1)
    # default_end = dt.date(2026, 2, 5)
    default_end = dt.date.today() 
    
    
    start_date_input = st.date_input("Start Date", default_start)
    end_date_input = st.date_input("End Date", default_end)
    
    # Expiry Dates
    st.subheader("Expiry Dates")
    # Using text input for flexibility, but could be date pickers formatted as string
    expirydate_near_input = st.text_input("Near Expiry (dd-Mmm-yyyy)", "24-Feb-2026")
    expirydate_next_input = st.text_input("Next Expiry (dd-Mmm-yyyy)", "30-Mar-2026")
    expirydate_far_input = st.text_input("Far Expiry (dd-Mmm-yyyy)", "28-Apr-2026")

    run_btn = st.button("Get Data")

def process_symbol(symbol, startn, endn, exp_near, exp_next, exp_far):
    # Convert date objects to string dd-mm-yyyy if they aren't already
    if isinstance(startn, dt.date):
        startn = startn.strftime("%d-%m-%Y")
    if isinstance(endn, dt.date):
        endn = endn.strftime("%d-%m-%Y")

    try:
        # Fetch data once
        with st.spinner(f"Fetching data for {symbol}..."):
            df_raw = future_oi_eod_data(symbol, startn, endn)
        
        if not df_raw:
             st.warning(f"No data returned for {symbol}")
             return pd.DataFrame()

        df_main = pd.DataFrame(df_raw)
        
        if df_main.empty:
             st.warning(f"Empty dataset received for {symbol}")
             return pd.DataFrame()

        # near expiry data...
        if 'FH_EXPIRY_DT' not in df_main.columns:
            st.error("Data Validation Error: 'FH_EXPIRY_DT' column missing.")
            return pd.DataFrame()

        df_near = df_main[['FH_TIMESTAMP','FH_EXPIRY_DT','FH_SYMBOL','FH_OPEN_INT','FH_UNDERLYING_VALUE']]
        df_near = df_near[df_near['FH_EXPIRY_DT'] == exp_near]

        # next expiry data...
        df_next = df_main[['FH_TIMESTAMP','FH_EXPIRY_DT','FH_SYMBOL','FH_OPEN_INT']]
        df_next = df_next[df_next['FH_EXPIRY_DT'] == exp_next]

        # far expiry data...
        df_far = df_main[['FH_TIMESTAMP','FH_EXPIRY_DT','FH_SYMBOL','FH_OPEN_INT']]
        df_far = df_far[df_far['FH_EXPIRY_DT'] == exp_far]

        # calculation 
        df_merged = df_near.merge(df_next, on=['FH_TIMESTAMP','FH_SYMBOL'], suffixes=('_near', '_next'))
        df_merged = df_merged.merge(df_far, on=['FH_TIMESTAMP','FH_SYMBOL'], how='left')
        df_merged = df_merged.rename(columns={'FH_OPEN_INT': 'FH_OPEN_INT_far'})

        # Ensure OI columns are numeric (coerce errors to 0) then compute Total_OI
        for col in ['FH_OPEN_INT_near', 'FH_OPEN_INT_next', 'FH_OPEN_INT_far']:
            if col in df_merged.columns:
                df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce').fillna(0).astype('int64')
            else:
                df_merged[col] = 0

        df_merged['Total_OI'] = df_merged[['FH_OPEN_INT_near', 'FH_OPEN_INT_next', 'FH_OPEN_INT_far']].sum(axis=1)
        df_final = df_merged[['FH_TIMESTAMP', 'FH_SYMBOL','Total_OI','FH_UNDERLYING_VALUE']] 

        # Parse timestamps robustly
        df_final.loc[:, 'FH_TIMESTAMP'] = pd.to_datetime(df_final['FH_TIMESTAMP'], dayfirst=True, errors='coerce')
        # Keep only rows with valid timestamps
        df_final = df_final.loc[df_final['FH_TIMESTAMP'].notna()]

        # Sort by timestamp
        df_final = df_final.sort_values('FH_TIMESTAMP')

        df_final['OI_Per_Chng'] = df_final['Total_OI'].pct_change().fillna(0) * 100
        df_final['OI_Per_Chng'] = df_final['OI_Per_Chng'].round(2)

        df_final['oi_chng'] = df_final['Total_OI'].diff().fillna(0).astype('int64')

        df_final['per_eq'] = df_final['FH_UNDERLYING_VALUE'].pct_change().fillna(0) * 100
        df_final['per_eq'] = df_final['per_eq'].round(2)

        final_oi = df_final[['FH_TIMESTAMP','FH_SYMBOL','Total_OI','oi_chng','OI_Per_Chng','per_eq','FH_UNDERLYING_VALUE']]
        final_oi = final_oi.rename(columns={'FH_TIMESTAMP': 'DATE','FH_SYMBOL': 'SYMBOL','Total_OI':'TOTAL_OI','oi_chng': 'CHNG_OI','OI_Per_Chng': 'PER_OI','per_eq': 'PER_EQ','FH_UNDERLYING_VALUE':'CLOSE_PRICE'})
        
        return final_oi

    except Exception as e:
        st.error(f"Error processing {symbol}: {e}")
        return pd.DataFrame()


if run_btn:
    result_df = process_symbol(
        selected_symbol, 
        start_date_input, 
        end_date_input, 
        expirydate_near_input, 
        expirydate_next_input, 
        expirydate_far_input
    )

    if not result_df.empty:
        st.success(f"Data for {selected_symbol} loaded successfully!")
        
        # Format DATE column for better display if it's datetime
        # result_df['DATE'] = result_df['DATE'].dt.strftime('%d-%b-%Y')
        
        st.dataframe(result_df, width="stretch", hide_index=True)
        
        st.subheader("Total Open Interest (TOTAL_OI)")
        st.line_chart(result_df, x="DATE", y="TOTAL_OI")

       
    else:
        st.info("No data found matching the criteria. Please check dates and expiry inputs.")

  




