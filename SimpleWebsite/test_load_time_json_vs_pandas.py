import requests
import pandas as pd
import json
import timeit

def timeit_decorator(f):
    def wrapper(rt):
        start = timeit.default_timer()
        f(rt)
        stop = timeit.default_timer()
        delta = stop - start
        print('function={}. RunTime: '.format(f.__name__), delta) 
    return wrapper 

@timeit_decorator
def t_pandas(rt):    
    df = pd.read_json(rt)
    data = df['Value'].to_list()
    labels = df['DateTime'].apply(lambda x: x.strftime('%Y-%m-%d')).to_list()
    return data, labels

@timeit_decorator
def t_json(rt):
    _json = json.loads(rt) 
    data_labels = [(item['Value'], item['DateTime']) for item in _json]
    data, labels = zip(*data_labels)
    return list(data), [x.split('T')[0] for x in labels]

if __name__ == "__main__":
    base_url = 'https://api.tradingeconomics.com/historical/country/mexico/indicator/gdp'
    headers = {'Authorization': 'Client guest:guest'}    
    params = {'f': 'json'}
    r = requests.get(url=base_url, headers=headers, params=params)
    t_pandas(r.text)
    t_json(r.text)