# Importing all neccessary libraries
import streamlit as st 
import pandas as pd
import altair as alt
import docx2txt
import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objs as plts
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#from pypfopt import expected_returns, risk_models, EfficientFrontier
###from pypfopt.cla import CLA
from PIL import Image
import numpy as np
import pickle
from pypfopt import expected_returns, risk_models, plotting, EfficientFrontier
import plotly.graph_objs as go
from plotly.subplots import make_subplots


st.markdown(""" <div style="background-color:#d3f4e7;padding:10px ">
                    <h1 style=" color:#ff8043;text-align:center;font-size:26px"> Stock Price Forcasting and Portfolio Optimization App<br>Data-690 </h1>
                    <h2 style=" color:#ff8043;text-align:center;font-size:16px"> Group Members:<br>xx<br>yy<br>zz </h1>
                    </div> """,unsafe_allow_html=True)
        #Load image 
img = Image.open("/content/churn.png")
st.image(img, width = 705)
st.markdown("""<h1 style=" color:#ff8043;text-align:center;font-size:16px"> This app retrieves stock data from Yahoo Finance, performs Portifolio Optmization, stock price forcasting,Analysis of the most trending stock of the day</h1>""",unsafe_allow_html=True)

            
        
st.subheader("**Introduction**")
st.write("""Stock market prediction is the act of trying to determine the future value of a 
            company stock or other financial instrument traded on an exchange. """)



st.write("""The main objective of this project is -----------------.  """)


Select_dropdown = st.selectbox('**SELECT CONTENTS**',['Portifolio Optimization','Stock Price Forcasting', 'Trending Stock Analysis'])

if Select_dropdown == 'Portifolio Optimization':
    st.subheader('Portifolio Optimization')
    
    Menu = st.sidebar.radio("Menu",("Stocks Overview","Visualization","Sharpe Ratio","DDD","EEEE"))
@st.cache_data
def get_stock_data(symbols, start_date, end_date):
    data_dict = {}
    for symbol in symbols:
        data_dict[symbol] = yf.download(symbol, start=start_date, end=end_date)
    return data_dict

st.markdown("""<h1 style=" color:#ff8043;text-align:center;font-size:14px"> Enter ticker symbols and date range for the stocks you want to analyze</h1>""",unsafe_allow_html=True)
symbols = st.text_input('Enter Stock Symbols (e.g., AAPL, MSFT, GOOG):').split(',')
start_date = st.text_input('Enter Start Date (YYYY-MM-DD):')
end_date = st.text_input('Enter End Date (YYYY-MM-DD):')

def display_data_as_table(data):
    # Convert the data dictionary to a pandas DataFrame
    df = pd.concat(data, axis=1)
    df.index.name = 'Date'

    # Display the DataFrame using st.dataframe
    st.dataframe(df.head())


def get_stock_data(symbols, start_date, end_date):
    data_dict = {}
    for symbol in symbols:
        data_dict[symbol] = yf.download(symbol, start=start_date, end=end_date)
    return data_dict

import datetime
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_stock_data(symbols, start_date, end_date):
    data_dict = {}
    for symbol in symbols:
        data_dict[symbol] = yf.download(symbol, start=start_date, end=end_date)
    return data_dict

def plot_stock_prices(data):
    fig = go.Figure()
    for symbol, df in data.items():
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=symbol))
    fig.update_layout(
        title='Stock Prices',
        xaxis_title='Date',
        yaxis_title='Price',
        legend=dict(x=0, y=1, traceorder='normal')
    )
    return fig

def calculate_annualized_return(data):
    annualized_return = pd.Series(dtype='float64')
    for symbol, df in data.items():
        stock_annualized_return = (df['Close'].iloc[-1] / df['Close'].iloc[0]) ** (1 / (len(df) / 252)) - 1
        annualized_return[symbol] = stock_annualized_return
    return annualized_return

def plot_annualized_return(annualized_return):
    fig = go.Figure(data=go.Scatter(x=annualized_return.index, y=annualized_return, mode='lines'))
    fig.update_layout(
        title='Annualized Return',
        xaxis_title='Stock',
        yaxis_title='Annualized Return',
        legend=dict(x=0, y=1, traceorder='normal')
    )
    return fig

data = get_stock_data(symbols, start_date, end_date)
if Menu == "Stocks Overview":
    st.subheader('Data Cleaning and Summary Statistics')
    for symbol, df in data.items():
      
        st.write(f"First five rows of data for stock {symbol}:")
        st.write(df.head())  # Display first five rows
        st.write(f"Descriptive statistics {symbol}:")
        if 'Close' in df.columns:
            st.write(df['Close'].describe())  # Display summary statistics if 'Close' column exists
        else:
            st.write("Close column not found in DataFrame.") # Display summary statistics
        
        

elif Menu == "Visualization":
   # Plot stock prices
    st.subheader("Stock Prices")
    stock_prices_fig = plot_stock_prices(data)
    st.plotly_chart(stock_prices_fig)

    # Calculate annualized return
    annualized_return = calculate_annualized_return(data)

    # Plot annualized return
    st.subheader("Annualized Return")
    annualized_return_fig = plot_annualized_return(annualized_return)
    st.plotly_chart(annualized_return_fig)

    # Display the annualized return
    st.write("Annualized Daily Return:")
    st.write(annualized_return)



elif Menu == "Sharpe Ratio":
    #sharpe ratio

