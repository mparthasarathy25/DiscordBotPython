#imports with methods labeled, some imports were for the full library
from discord import File, Embed
from discord.ext import commands, tasks
from sqlite3 import connect
from datetime import datetime, timedelta, date
from matplotlib.pyplot import xticks, yticks, xlabel, ylabel, show, close, bar, savefig, plot, figure, title
import numpy as np
from io import BytesIO, StringIO
from os import remove, path, environ
from pandas import Index, DataFrame, read_csv, concat
from requests import get
from random import randint
from scipy.stats import norm

#creating the bot and setting the value of the 'client' variable to the bot
client = commands.Bot(command_prefix = '$', case_insensitive = True)

#reading in the tickers.csv, which includes symbol names (the main purpose)
ticker_data = read_csv('tickers.csv')
for element in range(len(ticker_data)):
        #setting a global dictionary as to make it easier to create every variable
        globals()[f"count_{element}"] = 0
        globals()[f"count_{element}_unique"] = 0

#global trace_list for the tracing api
global trace_list
trace_list = []



"""
A method used when the discord bot first goes online

...

Attributes
----------
N/A

Description
-----------
This method will insert each message from the discord server's relevant channels into a SQLlite database.
It will also iterate through each message to determine if there is a keyword match. If there is, the message
will be traced using Pat's API. After these operations are completed, two counters are started. One counter is
for tracing (60 minute loop) and the other counter is for appending to the SQLlite database (5 minute loop).
"""
@client.event
async def on_ready():
    #connecting to the sqllite database
    db = connect('sigma7.sqlite')
    cursor = db.cursor()
    #creating a table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sigma7(
        member TEXT,
        message TEXT,
        date TEXT,
        keyword TEXT
        )
    ''')
    clear = ("DELETE FROM sigma7")
    #removing anything that was already in the database when the bot goes online
    cursor.execute(clear)
    market_channel = client.get_channel(852551268056825879)
    chat_channel = client.get_channel(862525581685948416)
    #for loop to iterate through each channel's history
    async for msg in market_channel.history(limit=10000):
        #inserting each message, if the author isn't a bot, into the sqllite database
        if not msg.author.bot:
            time = msg.created_at
            sql = ("INSERT INTO sigma7(member, message, date) VALUES(?,?,?)")
            val = (str(msg.author), str(msg.content), time.strftime('%Y-%m-%d %H:%M:%S')) 
            cursor.execute(sql,val)
    async for msg in chat_channel.history(limit=10000): 
        #inserting each message, if the author isn't a bot, into the sqllite database
        if not msg.author.bot:
            time = msg.created_at
            sql = ("INSERT INTO sigma7(member, message, date) VALUES(?,?,?)")
            val = (str(msg.author), str(msg.content), time.strftime('%Y-%m-%d %H:%M:%S')) 
            cursor.execute(sql,val)
    #channel = client.get_channel(854077038514929687)
    # async for msg in channel.history(limit=10000):
    #     if not msg.author.bot:
    #         time = msg.created_at
    #         sql = ("INSERT INTO sigma7(member, message, date) VALUES(?,?,?)")
    #         val = (str(msg.author), str(msg.content), time.strftime('%Y-%m-%d %H:%M:%S')) 
    #         cursor.execute(sql,val)
    
    #same idea as the previous for loops, except this time, adding the messages to the tracing api and the global count variables
    #to determine whether there is a keyword match, each message in the server is split and checked
    msg_authors = []
    async for msg in market_channel.history(limit = 10000, after = datetime.now() + timedelta(hours=5) - timedelta(weeks=2)):
        if not msg.author.bot:
            for element in range(len(ticker_data)):
                if ticker_data.get('Symbol')[element] == msg.content:
                    api_url_Trace = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content}'
                    trace_list.append(get(api_url_Trace).json())                    
                    if msg.author not in msg_authors:
                        msg_authors.append(msg.author)
                        globals()[f"count_{element}_unique"] += 1
                        break
                    globals()[f"count_{element}"] += 1
                else:
                    for i in range(len(msg.content.split())):
                        if ticker_data.get('Symbol')[element] == msg.content.split()[i]:
                            api_url_Trace = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content.split()[i]}'
                            trace_list.append(get(api_url_Trace).json())
                            if msg.author not in msg_authors:
                                msg_authors.append(msg.author)
                                globals()[f"count_{element}_unique"] += 1
                            globals()[f"count_{element}"] += 1
                        

    #same as the above for loops but for the other relevant channel 
    async for msg in chat_channel.history(limit = 10000, after = datetime.now() + timedelta(hours=5) - timedelta(weeks=2)):
        if not msg.author.bot:
            for element in range(len(ticker_data)):
                if ticker_data.get('Symbol')[element] == msg.content:
                    api_url_Trace = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content}'
                    trace_list.append(get(api_url_Trace).json())
                    if msg.author not in msg_authors:
                        msg_authors.append(msg.author)
                        globals()[f"count_{element}_unique"] += 1
                        break
                    globals()[f"count_{element}"] += 1
                else:
                    for i in range(len(msg.content.split())):
                        if ticker_data.get('Symbol')[element] == msg.content.split()[i]:
                            api_url_Trace = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content.split()[i]}'
                            trace_list.append(get(api_url_Trace).json())
                            if msg.author not in msg_authors:
                                msg_authors.append(msg.author)
                                globals()[f"count_{element}_unique"] += 1
                            globals()[f"count_{element}"] += 1
                            

    # async for msg in channel.history(limit = None, after = datetime.datetime.now() + datetime.timedelta(hours=5) - datetime.timedelta(weeks=2)):
    #     if not msg.author.bot:
    #         for element in range(len(ticker_data)):
    #             for i in range(len(msg.content.split())):
    #                 if ticker_data.get('Symbol')[element] == msg.content.split()[i]:
    #                     globals()[f"count_{element}"] += 1
    #                     break

    #commiting the changes to the database and starting the counter and trendcounter loop methods
    db.commit()
    cursor.close()
    db.close()  
    counter.start()
    trendcounter.start()

"""
A 60-min looped method that traces keyword matched messages.

...

Attributes
----------
N/A

Description
-----------
This method will perform one of the key operations described for the on_ready command: tracing matched messages.
However, rather than iterating through every message every 5 minutes, the method will run every 60 minutes, so as 
to make operations a little easier. This method is mainly for accounting for the newest messages.
"""
@tasks.loop(minutes = 60)
async def trendcounter():
    #resetting the global dictionary to all values of 0
    for element in range(len(ticker_data)):
        globals()[f"count_{element}"] = 0
    market_channel = client.get_channel(852551268056825879)
    chat_channel = client.get_channel(862525581685948416)
    channel = client.get_channel(854077038514929687)
    msg_authors = []
    #essentially this performs the same task as what was done in the on_ready command, except every 60 minutes
    async for msg in market_channel.history(limit = 10000, after = datetime.now() + timedelta(hours=5) - timedelta(weeks=2)):
        if not msg.author.bot:
            for element in range(len(ticker_data)):
                if ticker_data.get('Symbol')[element] == msg.content:
                    api_url_Trace = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content}'
                    trace_list.append(get(api_url_Trace).json())
                    if msg.author not in msg_authors:
                        msg_authors.append(msg.author)
                        globals()[f"count_{element}_unique"] += 1
                        break
                    globals()[f"count_{element}"] += 1
                else:
                    for i in range(len(msg.content.split())):
                        if ticker_data.get('Symbol')[element] == msg.content.split()[i]:
                            api_url_Trace_1 = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content.split()[i]}'
                            trace_list.append(get(api_url_Trace_1).json())
                            if msg.author not in msg_authors:
                                msg_authors.append(msg.author)
                                globals()[f"count_{element}_unique"] += 1
                            globals()[f"count_{element}"] += 1
    async for msg in chat_channel.history(limit = 10000, after = datetime.now() + timedelta(hours=5) - timedelta(weeks=2)):
        if not msg.author.bot:
            for element in range(len(ticker_data)):
                if ticker_data.get('Symbol')[element] == msg.content:
                    api_url_Trace_2 = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content}'
                    trace_list.append(get(api_url_Trace_2).json())
                    if msg.author not in msg_authors:
                        msg_authors.append(msg.author)
                        globals()[f"count_{element}_unique"] += 1
                        break
                    globals()[f"count_{element}"] += 1
                else:
                    for i in range(len(msg.content.split())):
                        if ticker_data.get('Symbol')[element] == msg.content.split()[i]:
                            api_url_Trace_3 = f'https://sigma7-trends.azurewebsites.net/api/trace?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg==&symbol={msg.content.split()[i]}'
                            trace_list.append(get(api_url_Trace_3).json())
                            if msg.author not in msg_authors:
                                msg_authors.append(msg.author)
                                globals()[f"count_{element}_unique"] += 1
                            globals()[f"count_{element}"] += 1
    # async for msg in channel.history(limit = 10000, after = datetime.datetime.now() + datetime.timedelta(hours=5) - datetime.timedelta(weeks=2)):
    #     if not msg.author.bot:
    #         for element in range(len(ticker_data)):
    #             for i in range(len(msg.content.split())):
    #                 if ticker_data.get('Symbol')[element] == msg.content.split()[i]:
    #                     globals()[f"count_{element}"] += 1
    #                     break


"""
A 5-min looped method that appends to the SQLlite database.

...

Attributes
----------
N/A

Description
-----------
This method will perform one of the key operations described for the on_ready command: appending to SQLlite.
Similar to the method above, this method will run every 60 minutes so as to make operations easier. 
This method is mainly for accounting for the newest messages.
"""
@tasks.loop(minutes = 60)
async def counter():
    #same task as the on_ready function, but every 60 minutes
    db = connect('sigma7.sqlite')
    cursor = db.cursor()
    market_channel = client.get_channel(852551268056825879)
    chat_channel = client.get_channel(862525581685948416)
    channel = client.get_channel(854077038514929687)
    async for msg in market_channel.history(limit = 10000, after = datetime.now() + timedelta(hours=5) - timedelta(minutes=5)):
        if not msg.author.bot:
            time = msg.created_at
            sql = ("INSERT INTO sigma7(member, message, date) VALUES(?,?,?)")
            val = (str(msg.author), str(msg.content), time.strftime('%Y-%m-%d %H:%M:%S')) 
            cursor.execute(sql,val)
    async for msg in chat_channel.history(limit = 10000, after = datetime.now() + timedelta(hours=5) - timedelta(minutes=5)):
        if not msg.author.bot:
            time = msg.created_at
            sql = ("INSERT INTO sigma7(member, message, date) VALUES(?,?,?)")
            val = (str(msg.author), str(msg.content), time.strftime('%Y-%m-%d %H:%M:%S')) 
            cursor.execute(sql,val)
    # async for msg in channel.history(limit = None, after = datetime.datetime.now() + datetime.timedelta(hours=5) - datetime.timedelta(minutes=5)):
    #     if not msg.author.bot:
    #         time = msg.created_at
    #         sql = ("INSERT INTO sigma7(member, message, date) VALUES(?,?,?)")
    #         val = (str(msg.author), str(msg.content), time.strftime('%Y-%m-%d %H:%M:%S')) 
    #         cursor.execute(sql,val)
    db.commit()
    cursor.close()
    db.close()  

# def trending_unique():
#     x_trends = (first_trend, second_trend, third_trend, fourth_trend, fifth_trend)
#     pos = arange(len(x_trends))
#     numbers = [new_list[0],new_list[1],new_list[2],new_list[3],new_list[4]]
#     bar(pos, numbers, align = 'center')
#     xticks(pos, x_trends, color = 'white')
#     yticks(color = 'white')
#     ylabel('Number of Messages', color = 'white')
#     savefig('trend_image.png', transparent = True)
#     close()
#     with open('trend_image.png', 'rb') as f:
#         file = BytesIO(f.read())
    
#     image = File(file, filename = 'trend.png')
#     trending_embed = Embed(title = "Trending Stocks on Discord")
#     trending_embed.set_image(url = 'attachment://trend.png')
#     if path.exists('trend_image.png'):
#         remove('trend_image.png')
#     trending_embed.add_field(name = ("1. " + first_trend), value = ticker_data['Name'][company_index1].split()[0], inline = False)
#     trending_embed.add_field(name = ("2. " + second_trend), value = ticker_data['Name'][company_index2].split()[0], inline = False)
#     trending_embed.add_field(name = ("3. " + third_trend), value = ticker_data['Name'][company_index3].split()[0], inline = False)
#     trending_embed.add_field(name = ("4. " + fourth_trend), value = ticker_data['Name'][company_index4].split()[0], inline = False)
#     trending_embed.add_field(name = ("5. " + fifth_trend), value = ticker_data['Name'][company_index5].split()[0], inline = False)
#     return_list = [trending_embed, image]
#     return return_list


"""
A method that returns the trending stocks online and in discord.

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)

Description
-----------
This method will store the json output of the tracking api call, and a discord embed will be sent which contains the trending stocks.

"""
@client.command()
async def trending(ctx: commands.Context):
    #capturing data from the tracking api
    api_url_Track = 'https://sigma7-trends.azurewebsites.net/api/pull_symbols?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg=='
    #converting the json output to something viewable
    df_Track = get(api_url_Track).json()
    trending_test_embed = Embed(title = "Trending Stock (not in order)")
    #running a for loop and adding a field for each trending stock in the api call
    for i in range(len(df_Track)):
        # ticker = df_Track[i]
        # iex_api_key = 'Tsk_30a2677082d54c7b8697675d84baf94b'
        # api_url = f'https://sandbox.iexapis.com/stable/ref-data/options/symbols/{ticker}/?token={iex_api_key}'
        # df1 = get(api_url).json()
        trending_test_embed.add_field(name = (f"{i+1}."), value = df_Track[i], inline = False)
    await ctx.send(embed = trending_test_embed)  
    # ticker_data = read_csv('tickers.csv')
    # db = connect('sigma7.sqlite')
    # cursor = db.cursor()  
    # currentDate = date.today()
    # days = timedelta(14)
    # pastDate = currentDate - days
    # cursor.execute("SELECT message FROM sigma7 WHERE CAST(date as DATE) >= CAST(" + pastDate.strftime('%Y-%m-%d') + " as DATE)")
    # result3 = cursor.fetchall()
    # db.commit()
    # cursor.close()
    # list = []
    # first_trend = ""
    # second_trend = ""
    # third_trend = ""
    # fourth_trend = ""
    # fifth_trend = ""
    # for element in range(len(ticker_data)):
    #     list.append(globals()[f"count_{element}"])
    # list.sort(reverse = True)
    # new_list = list.copy()
    # for element in range(len(ticker_data)):
    #     if globals()[f"count_{element}"] == list[0]:
    #         first_trend = ticker_data.get('Symbol')[element]
    #         list[0] = -1
    #     elif globals()[f"count_{element}"] == list[1]:
    #         second_trend = ticker_data.get('Symbol')[element]
    #         list[1] = -1
    #     elif globals()[f"count_{element}"] == list[2]:
    #         third_trend = ticker_data.get('Symbol')[element]
    #         list[2] = -1
    #     elif globals()[f"count_{element}"] == list[3]:
    #         fourth_trend = ticker_data.get('Symbol')[element]
    #         list[3] = -1
    #     elif globals()[f"count_{element}"] == list[4]:
    #         fifth_trend = ticker_data.get('Symbol')[element]
    #         list[4] = -1

    # data_index = Index(ticker_data['Symbol'])
    # company_index1 = data_index.get_loc(first_trend)
    # company_index2 = data_index.get_loc(second_trend)
    # company_index3 = data_index.get_loc(third_trend)
    # company_index4 = data_index.get_loc(fourth_trend)
    # company_index5 = data_index.get_loc(fifth_trend)
    # x_trends = (first_trend, second_trend, third_trend, fourth_trend, fifth_trend)
    # pos = arange(len(x_trends))
    # numbers = [new_list[0],new_list[1],new_list[2],new_list[3],new_list[4]]
    # bar(pos, numbers, align = 'center')
    # xticks(pos, x_trends, color = 'white')
    # yticks(color = 'white')
    # ylabel('Number of Messages', color = 'white')
    # savefig('trend_image.png', transparent = True)
    # close()
    # with open('trend_image.png', 'rb') as f:
    #     file = BytesIO(f.read())
    
    # image =File(file, filename = 'trend.png')
    # trending_embed = Embed(title = "Trending Stocks on Discord")
    # trending_embed.set_image(url = 'attachment://trend.png')
    # if path.exists('trend_image.png'):
    #     remove('trend_image.png')
    # trending_embed.add_field(name = ("1. " + first_trend), value = ticker_data['Name'][company_index1].split()[0], inline = False)
    # trending_embed.add_field(name = ("2. " + second_trend), value = ticker_data['Name'][company_index2].split()[0], inline = False)
    # trending_embed.add_field(name = ("3. " + third_trend), value = ticker_data['Name'][company_index3].split()[0], inline = False)
    # trending_embed.add_field(name = ("4. " + fourth_trend), value = ticker_data['Name'][company_index4].split()[0], inline = False)
    # trending_embed.add_field(name = ("5. " + fifth_trend), value = ticker_data['Name'][company_index5].split()[0], inline = False)
    # await ctx.send(embed = trending_embed, file = image)

"""
A helper method that will create a graph of a company's pricing data for a certain period of time.

...

Attributes
----------
symbol: String, company symbol
length: String, length of time
method: String, open, high, low, close

Description
-----------
This method will use the iexcloud api's data for charting graphs. Additionally, I have added each method 
to a separate concatenated variable, which allows for the inputted method to be used in creating the graphs.

"""
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
    
    #for loop to add data to a list for charting graphs
    for i in range(len(df)):
        date.append(df[i]['date'])
        open.append(df[i]['open'])
        high.append(df[i]['high'])
        low.append(df[i]['low'])
        close1.append(df[i]['close'])
    
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

"""
A method that has two options: graph and updates.

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
company_name: String, company symbol
option: String, graph or updates
method: String, high, low, open, close
length: String, length of time

Description
-----------
The graph option uses the get_historic_data helper method and adds the image to a discord embed. 
The updates method uses the iexcloud api data and simply outputs the data in a different form.

"""
@client.command()
async def stock(ctx: commands.Context, company_name, option, method = '', length = ''):
    # ticker = yf.Ticker(company_name)
    # delta = datetime.timedelta(days = 30)
    # delta1 = datetime.timedelta(days = 1)
    # dates = drange(date.today()-delta, date.today(), delta1)
    # prices = ticker.history(period = "30d").get('Open')

    #if statement for the different operations
    if option == 'graph':
        #try statement for an assertion error with the company_name
        try:
            assert company_name != None
        except AssertionError:
            ctx.send("In order to use this command, you must input a company ticker name, for example AAPL")
        
        #try statement for an assertion error with the method
        try:
            assert method != ''
        except AssertionError:
            ctx.send("In order to use this command, you must input a method, for example low")
        
        #try statement for an assertion error with the length
        try:
            assert length != ''
        except AssertionError:
            ctx.send("In order to use this command, you must input a length, for example 1d")
        if method != '':
            if length != '':
                #using the get_historic_data helper method to graph
                get_historic_data(company_name, length, method)
                embed = Embed(title= method.capitalize() + ' Price Change Of ' + company_name + ' Over The Last ' + length, colour= 0x00b2ff)
                with open('stock_image.png', 'rb') as f:
                    file = BytesIO(f.read())
                if path.exists('stock_image.png'):
                    remove('stock_image.png')
                image = File(file, filename='graph' + company_name + '.png')
                embed.set_image(url=f'attachment://graph' + company_name + '.png')
                #sending the embed with the image
                await ctx.send(embed=embed,file=image)
    #update operation
    elif option == 'updates':
        #try statement for an assertion error with the company_name
        try:
            assert company_name != None
        except AssertionError:
            ctx.send("In order to use this command, you must input a company ticker name, for example AAPL")
        ticker = company_name
        # IEX_KEY = ""
        # token = environ["IEX_KEY"]
        #using iex cloud api data for latest price, market cap, etc.
        iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
        api_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/quote/?token={iex_api_key}'
        df = get(api_url).json()
        api_url1 = f'https://cloud.iexapis.com/stable/time-series/CORE_ESTIMATES/{ticker}/?token={iex_api_key}'
        df1 = get(api_url1).json()
        embed = Embed(title='Latest Updates of ' + ticker, colour= 0x00b2ff)
        embed.add_field(name = "Symbol : " + str(df['symbol']), value = "Latest Price : " + str(df['latestPrice']) + "\n" + "Market Cap : " + str(df['marketCap']) + "\n" + "Percent Change (from last close) : " + str(df['changePercent']) + "\n" + "Market Consensus : " + str(df1[0]['marketConsensus']))
        await ctx.send(embed = embed)


"""
A method that will print out news articles given a stock ticker

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
company_name: String, company symbol
number: int, number of articles to be printed

Description
-----------
This method will use the polygon api and will print out news articles dependent on how many articles to be printed.
The discord embed that will be outputed prints out the title, article_url, description, and image.

"""
api = '3c3wFYiCLgsFup0dHv0p4kxJnSVx_mrG'
@client.command()
async def news(ctx: commands.Context, company_name, number: int = 5):
    #try statement for an assertion error with the company_name
    try:
        assert company_name != None
    except AssertionError:
        ctx.send("In order to use this command, you must input a company name, for example AAPL")

    bool_test = False
    data_index = Index(ticker_data['Symbol'])
    company_index = data_index.get_loc(company_name)

    ticker = company_name
    limit = '100'
    #using the api from polygon to get the news
    api_url = f'https://api.polygon.io/v2/reference/news?limit={limit}&order=descending&sort=published_utc&ticker={ticker}&published_utc.gte=2021-04-26&apiKey={api}'
    data = get(api_url).json()
    count = 0
    #iterating the resulting news data
    for element in data['results']:
        if count >= number:
            break
        if (ticker_data['Name'][company_index].split()[0].lower()) in element['article_url']:
            #using try statements for if there aren't descriptions or image_urls
            try: 
                element['description']
            except KeyError:
                discord_embed = Embed(title= element['title'], url= element['article_url'])
            else:
                discord_embed = Embed(title= element['title'], url= element['article_url'],  description = element['description'])
            try:
                element['image_url']
            except KeyError:
                continue
            else:
                discord_embed.set_image(url = element['image_url'])
            #sending the discord embed
            await ctx.send(embed = discord_embed)
            count += 1

"""
A method that will round a number to however many decimal places

...

Attributes
----------
n: int, number to be rounded
decimals: int, decimal to be rounded to

Description
-----------
This method take a number and use the decimals variable to divide until the correct number of decimal places is reached.

"""
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    #returning the correctly rounded number
    return int(n * multiplier) / multiplier

member_list = []
portfolio_list = []

"""
A method that holds a user's portfolio in discord

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
option: String, create, update, view
items: String, items for the portfolio

Description
-----------
This method will create a portfolio by appending each user's portfolio
to a portfolio list. Then, if the same user asks to view their portfolio,
the portfolio list will be matched to the member list position. Same goes 
for the update method, where the user can add or remove from their previously
created portfolio.

"""
@client.command()
async def portfolio(ctx: commands.Context, option, *, items=''):
    stock_list = []
    portfolio_embed = Embed(title = "Your Portfolio")
    #appending the author to the member list
    member_list.append(ctx.author.display_name)
    #iterating through the member list to add number to portfolio list
    for i in range(len(member_list)):
        portfolio_list.append(i)
    
    #if statement for the different options
    if option == "create":
        #try statement for an assertion error with the items
        try:
            assert items != ''
        except AssertionError:
            ctx.send("In order to create a portfolio, you must add stock items, for example: MSFT 2")
        if len(items.split()) != 0:
            for i in range(len(items.split())):
                if i % 2 == 0:  
                    iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
                    api_url = f'https://cloud.iexapis.com/stable/stock/{items.split()[i]}/quote/?token={iex_api_key}'
                    df = get(api_url).json()
                    #essentially reprinting the items but in a form where you can view the latest price of the shares the user owns
                    portfolio_embed.add_field(name = (items.split()[i+1] + " shares of " + items.split()[i]), value = "$" + str(truncate((int(items.split()[i+1])*int(df['latestPrice'])), 2)), inline = True)
                    stock_list.append(items.split()[i])
        
        #portfolio_list.append(portfolio_embed)
        #setting the index of the member_list to the portfolio_embed, so the two lists match
        portfolio_list[member_list.index(ctx.author.display_name)] = portfolio_embed
        await ctx.author.send(embed = portfolio_list[member_list.index(ctx.author.display_name)])
    elif option == "update":
        #try statement for an assertion error with the items
        try:
            assert items != ''
        except AssertionError:
            ctx.send("In order to update a portfolio, you must describe what you want to update, for example: add AAPL 2 remove 1")
        count = 0 
        if len(items.split()) != 0:
            for i in range(len(items.split())):
                #essentially performing the same task as create, but add will input more into the embed, while remove will take away
                #using split in a lot of these situations to run through a string and see if there are relevant matches
                if items.split()[i] == "add":
                    for item in items.split()[(i+1):]:
                        if item == "remove":
                            break
                        elif i+1 % 2 == 0:
                            if items.split().index(item) % 2 == 0:
                                iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
                                api_url = f'https://cloud.iexapis.com/stable/stock/{items.split()[items.split().index(item)]}/quote/?token={iex_api_key}'
                                df = get(api_url).json()
                                portfolio_list[member_list.index(ctx.author.display_name)].add_field(name = (items.split()[items.split().index(item)+1] + " shares of " + items.split()[items.split().index(item)]), value = "$" + str(truncate(int(items.split()[items.split().index(item)+1])*df['latestPrice'], 2)), inline = True)
                        elif i+1 % 2 == 1:
                            if items.split().index(item) % 2 == 1:
                                iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
                                api_url = f'https://cloud.iexapis.com/stable/stock/{items.split()[items.split().index(item)]}/quote/?token={iex_api_key}'
                                df = get(api_url).json()
                                portfolio_list[member_list.index(ctx.author.display_name)].add_field(name = (items.split()[items.split().index(item)+1] + " shares of " + items.split()[items.split().index(item)]), value = "$" + str(truncate(int(items.split()[items.split().index(item)+1])*df['latestPrice'], 2)), inline = True)            

                elif items.split()[i] == "remove":
                    for item in items.split()[(i+1):]:
                        if item == "add":
                            break
                        elif count == 0:
                            portfolio_list[member_list.index(ctx.author.display_name)].remove_field(int(item) - 1)
                            count += 1
                        elif count > 0:
                            portfolio_list[member_list.index(ctx.author.display_name)].remove_field(int(item) - 1 - count)
                            count += 1


        await ctx.author.send(embed = portfolio_list[member_list.index(ctx.author.display_name)])


    elif option == "view":
        await ctx.author.send(embed = portfolio_list[member_list.index(ctx.author.display_name)])

"""
A method that will return a random number from 1 to n, a roll of a dice

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
number: int, number of sides to roll

Description
-----------
This method will simply perform the randint method and return a message of what number was rolled.

"""
@client.command()
async def roll(ctx: commands.Context, number: int = 6):
    #randint
    await ctx.send("Here's your lucky number: " + str(randint(1,number)))


"""
A method that will return the description of a specific company

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
company_name: String, company symbol

Description
-----------
This method will use the iex cloud api method and return a description from the json output.

"""
@client.command()
async def description(ctx: commands.Context, company_name):
    #try statement for an assertion error with the company_name
    try:
        assert company_name != None
    except AssertionError:
        ctx.send("In order to use this command, you must input a company name, for example AAPL")
    iex_api_key = 'pk_6fdc6387a2ae4f8e9783b029fc2a3774'
    api_url = f'https://cloud.iexapis.com/stable/stock/{company_name}/company/?token={iex_api_key}'
    df = get(api_url).json()
    desc_embed = Embed(title = company_name)
    #add field with the description
    desc_embed.add_field(name = 'Description', value = df['description'])
    await ctx.send(embed = desc_embed)


"""
A method that will simulate a company's price performance over the future 30 days.

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
company_name: String, company symbol

Description
-----------
This method takes in data from the iex cloud for the past 5 years, and takes in the pct change for
each day. Then, the mean and stdev of the pct changes are taken. After this, 10 simulations are done
based off of the probability distribution of the returns (pct changes). The 10 simulations are graphed
with the same starting point, being the previous day's close.

"""
@client.command()
async def simulation(ctx: commands.Context, company_name):
    #try statement for an assertion error with the company name
    try:
        assert company_name != None
        assert company_name != " "
    except AssertionError:
         ctx.send("In order to use this command, you must input a company name, for example AAPL")
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
    embed = Embed(title= 'Monty Carlo Simulation of the Close Price Change Of ' + company_name + ' Over The Last 30 Days (Each Line Represents a Different Simulation)', colour= 0x00b2ff)
    with open('sim_image.png', 'rb') as f:
        file = BytesIO(f.read())
    if path.exists('sim_image.png'):
        remove('sim_image.png')
    image = File(file, filename='graphsim' + company_name + '.png')
    embed.set_image(url=f'attachment://graphsim' + company_name + '.png')
    await ctx.send(embed=embed,file=image)

    
"""
A method that will print out all commands that can be printed. 

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)

Description
-----------
This method that returns the command list and examples in a discord embed.

"""
@client.command()
async def allcommands(ctx: commands.Context):
    command_embed = Embed(title = 'Available Commands')
    command_embed.add_field(name = 'Command List: ', value = '$trending \n$news tickername numberofarticles \n$stock tickername (graph or updates) (if graph, choose what to graph: low, high, close, open) (if graph, choose time period: 5d, 1m, 3m, 1y)  \n$portfolio (create or update or view) (if create, input the ticker followed by how many shares owned; ex: AAPL 2 MSFT 3) <- (If update instead of create, input add (add MSFT 3 NFLX 2) or remove (remove 1, will remove first stock in portfolio) \n$simulation tickername \n$description tickername \n$roll number')
    command_embed.add_field(name = 'Examples: ', value = 'Examples: \n$trending \n$news AAPL 3 \n$stock GS updates \n$stock GS graph low 3d \n$portfolio create MSFT 3 GOOGL 5 AA 2 \n$portfolio update add AAPL 3 \n$portfolio update remove 1 \n$portfolio update add NFLX 2 remove 2 \n$portfolio view \n$simulation AAPL \n$description NFLX \n$roll 6')
    await ctx.send(embed = command_embed)
    

"""
A method that will purge messages in the server. This method is only for people who can manage messages in the server.

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
number: int, number of messages to delete

Description
-----------
This method will remove a specified number of messages in the channel the message was sent in. 

"""
@client.command()
async def purge(ctx: commands.Context, *, number:int=None):
    if ctx.message.author.guild_permissions.manage_messages:
        try:
            if number is None:
                await ctx.send("You must input a number")
            else:
                deleted = await ctx.message.channel.purge(limit = number)
                await ctx.send(f"Messages purged by {ctx.message.author.mention}: '{len(deleted)}'")
        except:
            await ctx.send("I can't purge messages here.")
    else:
        await ctx.send("You do not have permissions to use this command.")


"""
An error method

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
error: String, command

Description
-----------
If CommandNotFound error is thrown, an error message will be sent in discord

"""
@client.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I'm not sure what that means...")


"""
An error method

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
error: String, command

Description
-----------
If CommandNotFound error is thrown, an error message will be sent in discord.
If MissingRequiredArgument error is thrown, an error message will be sent in discord.

"""
@portfolio.error
async def portfolio_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you're missing something...")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I think you typed something wrong...")


"""
An error method

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
error: String, command

Description
-----------
If CommandNotFound error is thrown, an error message will be sent in discord
If MissingRequiredArgument error is thrown, an error message will be sent in discord.

"""
@stock.error
async def stock_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you're missing something...")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I think you typed something wrong...")


"""
An error method

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
error: String, command

Description
-----------
If CommandNotFound error is thrown, an error message will be sent in discord
If MissingRequiredArgument error is thrown, an error message will be sent in discord.

"""
@news.error
async def news_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you're missing something...")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I think you typed something wrong...")


"""
An error method

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
error: String, command

Description
-----------
If CommandNotFound error is thrown, an error message will be sent in discord
If MissingRequiredArgument error is thrown, an error message will be sent in discord.

"""
@roll.error
async def roll_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you're missing something...")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I think you typed something wrong...")


"""
An error method

...

Attributes
----------
ctx: commands.Context (allows for the returned message to be sent wherever the command was made.)
error: String, command

Description
-----------
If CommandNotFound error is thrown, an error message will be sent in discord
If MissingRequiredArgument error is thrown, an error message will be sent in discord.

"""
@description.error
async def description_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you're missing something...")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("I think you typed something wrong...")


client.run('ODUzODY1MDkyNTg4NjM0MTMz.YMbl1g.NR_nKTOXqiP4NBwpov9zw-mFYtU')
