from flask import Flask
from flask import render_template
#https://flask.palletsprojects.com/en/2.2.x/
import requests 
#https://requests.readthedocs.io/en/latest/
import json

app = Flask(__name__)

def _get_mexico_gdp_from_tradingEconomics_api():
    # Note, tradingEconomics free developer account key/secret authorization does not work atm. 
    # Hence only guest account access is possible for now.
    #
    # Note, loading response body with json is much faster than loading into a pandas dataframe.
    # See test_load_time_json_vs_pandas.py
    base_url = 'https://api.tradingeconomics.com/historical/country/mexico/indicator/gdp'    
    headers = {'Authorization': 'Client guest:guest'}
    params = {'f': 'json'}
    r = requests.get(url=base_url, headers=headers, params=params)
    data_labels = [(item['Value'], item['DateTime']) for item in json.loads(r.text)]
    data, labels = zip(*data_labels)
    return list(data), [x.split('T')[0] for x in labels]   

@app.route("/")
def home():
    try:
        data, labels = _get_mexico_gdp_from_tradingEconomics_api()
        return render_template('home.html', labels=labels, data=data)    
    except Exception as e:                
        return "failure"
    
if __name__ == "__main__":
    app.run(debug=True)
    