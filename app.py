# pip install pandas numpy matplotlib streamlit pystan fbprophet cryptocmd plotly
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as data
import streamlit.components.v1 as components
import fbprophet
from fbprophet import Prophet
from datetime import date
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from keras.models import load_model
from PIL import Image
img=Image.open('logo.jpeg')
st.set_page_config(page_title='predict crypto price',page_icon=img)
hide_menu_style="""
 <style>
 #MainMenu {visibility:hidden;}
 footer{visibility:hidden;}
 </style>
 """
st.markdown(hide_menu_style,unsafe_allow_html=True)
start='2011-01-01'
end='2022-01-01'
today=date.today().strftime("%Y-%m-%d")
st.title("PREDICT THE CRYPTO PRICE AND TREND")
cryptos=("BTC-USD", "ETH-USD", "USDT-USD", "BNB-USD", "USDC-USD", "SOL-USD", "ADA-USD", "XRP-USD", "LUNA1-USD", "HEX-USD", "AVAX-USD", "DOT-USD", "DOGE-USD", "SHIB-USD", "MATIC-USD", "ATOM-USD", "LTC-USD")
targetcrypto=st.selectbox("ENTER THE CRYPTO TO BE PREDICTED",cryptos)
def load_data(ticker):
    data=yf.download(ticker,start,today)
    data.reset_index(inplace=True)
    return data
data_load_state=st.text("loading data...")
data=load_data(targetcrypto)
data_load_state.text("data loaded sucessfully....")
st.subheader("DATA FROM 2011 TO CURRENT DAY")
st.write(data.tail())
def org_graph():
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
    fig.layout.update(title_text="TILL DATE DATA",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
org_graph()
timeline=("WEEKS","MONTHS","YEARS")
duration=st.selectbox("ENTER THE DURATION TO PREDICT",timeline)
N=st.number_input("ENTER NUMBER",0,10)
if(duration=="WEEKS"):
    no_of_days=N*7
if(duration=="MONTHS"):
    no_of_days=N*30
if(duration=="YEARS"):
    no_of_days=N*365
df_train=data[['Date', 'Close']]
df_train=df_train.rename(columns={"Date":"ds","Close":"y"})
m= Prophet()
m.fit(df_train)
future=m.make_future_dataframe(periods=no_of_days)
forecast=m.predict(future)
st.subheader('PREDICTED DATA')
st.write(forecast.tail())
st.subheader('FORECAST DATA')
fig1=plot_plotly(m,forecast)
st.plotly_chart(fig1)
st.write("FORECAST COMPONENTS")
fig2=m.plot_components(forecast)
st.write(fig2)
