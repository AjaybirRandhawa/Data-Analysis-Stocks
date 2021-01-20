import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

#Creates the website
st.title('Stock Prices for S&P 500')
st.markdown(""" This app retrives the list of S&P500 index via webscrapping, then utilizes yfinance to find related stock information. Information will be displayed below as a dataset and as a graph. The datasets can be downloaded for personal use.
* **Python Libraries:** streamlit, pandas, matplotlib.pyplot and yfinance 
* **Usage:** To use this app please use the left sidebar and input required information. Please use Ticker Symbols for S&P500 Only.""")

#Creates area for user input
st.sidebar.title("User Input Features")

#Webscrapping wikipedia for S&P 500 names list
@st.cache
def load_wikipedia():
    """Upon starting, uses wikipedia's page on S&P500 to load names and a generalized dataset
    in:  None
    out: dataset containing all S&P500 companies
    """
    url ='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    dataset = html[0] #We only want the 1st table
    return dataset
def load_data(input_symbol, *args, input_period="ytd", input_interval="1d"):
    """Generates a pandas dataframe using information entered by user 
    in:  Ticker Symbol, period, interval
    out: pandas dataframe
    """
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = input_symbol,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = input_period,

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = input_interval,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,
    )
    return data
dataset = load_wikipedia()
unique_Sector = dataset['GICS Sector'].unique()
sectors = dataset.groupby('GICS Sector')

st.sidebar.subheader("Search the S&P 500")
value = ''
user_input = st.sidebar.text_input("Enter A Ticker Symbol:",value= value, max_chars=5)
periods = [ "1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "ytd", "max"]
input_periods = st.sidebar.select_slider('Select A Period (Default is YTD):', options=periods, value='ytd')
intervals = [ '1m', '2m', '5m', '15m', '30m' , '60m', '90m', '1h', '1d','5d', '1wk', '1mo','3mo']
input_intervals = st.sidebar.select_slider('Select A Period (Default is 1d):', options=intervals, value='1d')

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded.
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"""<a style="padding:15px 30px; padding-left: 4%;margin-left: 30%; color: rgb(93, 92, 160); background-color: lightcyan; text-transform: uppercase; letter-spacing: 4px; text-decoration: none; overflow: hidden; font-size: 15px;" href="data:file/csv;base64,{b64}">Download csv file</a><br><br><br>"""
    return href

def footer():
    """Generates a footer to be placed at the end of the document.
    in:  None
    out: href string
    """
    href= f"""This app was constructed by Ajaybir Randhawa as a means of displaying Data analysis, webscrapping and visualization tools usage. Checkout my<a style="text-decoration: none; overflow: hidden;" href="https://ajaybirrandhawa.github.io"> website </a>for other cool things!"""
    return href
def plot_data(df):
    """Plots the data using matplotlib.pyplot according to Date and Closing price.
    in:  dataframe
    out: matplot.pyplot figure
    """
    plt.fill_between(df.Date, df.Close, color="skyblue", alpha=0.3)
    plt.plot(df.Date, df.Close, color="skyblue", alpha=0.8)
    plt.xticks(rotation=90)
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    return plt

if st.sidebar.button("Search"):
    resulting_data = load_data(user_input, input_period=input_periods, input_interval=input_intervals)
    st.subheader(f"{user_input} Dataset")
    st.dataframe(resulting_data)
    dataset2 = pd.DataFrame(resulting_data.Close)
    dataset2['Date'] = dataset2.index
    st.subheader(f"{user_input}'s Graph of Closing Prices and Dates")
    st.pyplot(plot_data(dataset2))
    st.markdown(get_table_download_link(resulting_data), unsafe_allow_html=True)

st.markdown(footer(), unsafe_allow_html=True)