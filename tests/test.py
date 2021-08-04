import os
import sys
from requests import get

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import func

def test_trending():
    api_url_Track = 'https://sigma7-trends.azurewebsites.net/api/pull_symbols?code=O8f03FccQJ8csnd8KAHq0E6s9VTaaGXBJMyXfRjduOlUvCstecmowg=='
    assert func.trending() == get(api_url_Track).json()

def test_get_historic():
    list_data = func.get_historic_data('AAPL', '1y', 'low')
    assert list_data[0] != None
    assert list_data[1] != None
    assert list_data[2] != None
    assert list_data[3] != None
    assert list_data[4] != None

def test_stock():
    func.stock('AAPL','graph','low','1y')
    assert os.path.exists('stock_image.png') != True

def test_news():
    results = func.news('AAPL')
    ticker = 'AAPL'
    limit = '100'
    api = api = '3c3wFYiCLgsFup0dHv0p4kxJnSVx_mrG'
    api_url = f'https://api.polygon.io/v2/reference/news?limit={limit}&order=descending&sort=published_utc&ticker={ticker}&published_utc.gte=2021-04-26&apiKey={api}'
    assert results['results'] == get(api_url).json()['results']

def test_simulation():
    results = func.simulation('AAPL')
    assert os.path.exists('sim_image.png') != True
    assert results[0][0] <= 0.5
    assert results[0][0] <= 0.5


