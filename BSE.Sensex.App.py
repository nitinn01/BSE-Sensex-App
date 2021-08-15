import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import yfinance as yf
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('BSE Sensex Top 30 Companies App')
image = Image.open('logo.jpg')
st.image(image, width = 650)
st.markdown("""
*This app retrieves the list of the BSE Sensex 30 Companies and shows the performance of company's stock in current year(2021)*

**Description:  ** 
The objective of this application is  to provide insights into the overall trends of the BSE listed companies. It analyses the latest trend in major sectors by tracking the change in company's stock over a period of year on monthly basis. The user can visualize the performance and changes taking place in the stock market by selecting the industry and number of companies corresponding to each industry sector.
It can be tracked with the graphical representation of stocks plotted as per the changes in market.

*Data source:* [Wikipedia](https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of BSE Sensex data
#
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['Sector'].unique() )
selected_sector = st.sidebar.multiselect('Insdustry Sectors', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['Sector'].isin(selected_sector)) ]

st.header('BSE Listed Companies')
#st.write('Data Description: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download Indian Sensex Data data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
#def filedownload(df):
    #csv = df.to_csv(index=False)
    #b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    #href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    #return href

#st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Month', fontweight='bold')
  plt.ylabel('Stock Price  (₹) ', fontweight='bold')
  return st.pyplot()                

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header("Company's month-wise stock performance in 2021")
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)   
