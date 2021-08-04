from sqlite3 import connect
from datetime import datetime, timedelta, date
from matplotlib.pyplot import xticks, yticks, xlabel, ylabel, show, close, bar, savefig, plot, figure, title
import numpy as np
from io import BytesIO, StringIO
from os import remove, path, environ
from numpy.core.fromnumeric import std
from pandas import Index, DataFrame, read_csv, concat
from requests import get
from random import randint
from scipy.stats import norm

ticker_data = read_csv('tickers.csv')

def trending():
    api_url_Track = 'https://sigma7-trends.azurewebsites.net/api/pull_symbols?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg=='
    df_Track = get(api_url_Track).json()
    return df_Track


def get_historic_data(symbol, length, method):
    #using the iex cloud api
    iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
    api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/chart/{length}?token={iex_api_key}'
    #converting the json output
    df = get(api_url).json()
    
    date = []
    open = []
    high = []
    low = []
    close1 = []
    
    lst = []

    #for loop to add data to a list for charting graphs
    for i in range(len(df)):
        date.append(df[i]['date'])
        open.append(df[i]['open'])
        high.append(df[i]['high'])
        low.append(df[i]['low'])
        close1.append(df[i]['close'])
    
    lst.append(date)
    lst.append(open)
    lst.append(high)
    lst.append(low)
    lst.append(close1)
    #renaming the columns for a future command
    date_df = DataFrame(date).rename(columns = {0:'date'})
    open_df = DataFrame(open).rename(columns = {0:'open'})
    high_df = DataFrame(high).rename(columns = {0:'high'})
    low_df = DataFrame(low).rename(columns = {0:'low'})
    close_df = DataFrame(close1).rename(columns = {0:'close'})
    
    #concatenating the lists to one
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = concat(frames, axis = 1, join = 'inner')
    df = df.set_index('date')
    
    #plotting the graph given the method and making stylistic changes
    df[method].plot()
    xlabel('Date', fontsize = 10, color = 'white')
    ylabel('Price', fontsize = 10, color = 'white')
    xticks(fontsize = 8, color = 'white')
    yticks(fontsize = 10, color = 'white')
    savefig('stock_image.png', transparent = True)
    close()
    return lst

def stock(company_name, option, method = '', length = ''):
    # ticker = yf.Ticker(company_name)
    # delta = datetime.timedelta(days = 30)
    # delta1 = datetime.timedelta(days = 1)
    # dates = drange(date.today()-delta, date.today(), delta1)
    # prices = ticker.history(period = "30d").get('Open')

    #if statement for the different operations
    if option == 'graph':
        if method != '':
            if length != '':
                #using the get_historic_data helper method to graph
                list_data = get_historic_data(company_name, length, method)
                with open('stock_image.png', 'rb') as f:
                    file = BytesIO(f.read())
                if path.exists('stock_image.png'):
                    remove('stock_image.png')
                #sending the embed with the image
    #update operation
    elif option == 'updates':
        ticker = company_name
        iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
        api_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/quote/?token={iex_api_key}'
        df = get(api_url).json()
        api_url1 = f'https://cloud.iexapis.com/stable/time-series/CORE_ESTIMATES/{ticker}/?token={iex_api_key}'
        df1 = get(api_url1).json()


api = '3c3wFYiCLgsFup0dHv0p4kxJnSVx_mrG'
def news(company_name):
    bool_test = False
    data_index = Index(ticker_data['Symbol'])
    company_index = data_index.get_loc(company_name)

    ticker = company_name
    limit = '100'
    #using the api from polygon to get the news
    api_url = f'https://api.polygon.io/v2/reference/news?limit={limit}&order=descending&sort=published_utc&ticker={ticker}&published_utc.gte=2021-04-26&apiKey={api}'
    data = get(api_url).json()
    return data

def simulation(company_name):
    #using iex cloud api to take historic data
    iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
    api_url = f'https://cloud.iexapis.com/stable/stock/{company_name}/chart/5y/?token={iex_api_key}'
    df = get(api_url).json()
    data = concat([DataFrame([df[i]['close']], columns=['Close']) for i in range(len(df))],
            ignore_index=True)
    #calculating the percent change day-to-day
    returns = data.pct_change()
    returns.dropna(inplace = True)
    l = norm.ppf(0.10)
    u = norm.ppf(0.85)
    #taking mean and standard deviation, which will help with probability distribution
    mean = returns.mean()
    stdev = returns.std()
    np.random.seed(42)
    n = np.random.normal(size = (30,10))
    rows = n.shape[0]
    cols = n.shape[1]
    #for loop to sift through the random.normal
    for i in range(0,rows) :
        for j in range(0,cols) :
            #with the upper limit and lower limit, restrictions are made
            if n[i][j] > u :
                n[i][j] = u       #sets upper limit
            elif n[i][j] < l :
                n[i][j] = l     #sets lower limit
            else :
                n[i][j] = n[i][j]
            n[i][j] = (stdev * n[i][j]) + mean
    s = data.iloc[-1]
    pred = np.zeros_like(n) + 1
    #sets beginning point of simulations
    pred[0] = s        
    #for each of the 30 days, setting the data by looking at i-1 data 
    for i in range(1,30) :
        pred[i] = pred[(i-1)] * (1 + n[(i-1)])  
    for i in range(0,10) :
        plot(pred[:, i])
    xlabel('Days Past Present', fontsize = 10, color = 'white')
    ylabel('Close Price', fontsize = 10, color = 'white')
    xticks(fontsize = 8, color = 'white')
    yticks(fontsize = 10, color = 'white')
    savefig('sim_image.png', transparent = True)
    close()
    with open('sim_image.png', 'rb') as f:
        file = BytesIO(f.read())
    if path.exists('sim_image.png'):
        remove('sim_image.png')
    return mean, stdev

