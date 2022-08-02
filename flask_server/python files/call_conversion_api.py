import json
import time
from pymongo import MongoClient
import certifi
from API_Key import API_KEY
import requests
import parallel
import concurrent.futures
from compute_arbitrage import Arbitrage

cluster = MongoClient('mongodb+srv://mann:mann1234@cluster0.bdk55.mongodb.net/?retryWrites=true&w=majority',
                      tlsCAFile=certifi.where())

mdb_db = cluster['currency_exchange_data']
mdb_symbols = mdb_db['symbols']

mdb_hist_data = mdb_db['historical_data']  # Historical Data Collection


def get_conversion(convert_to, base):
    payload = {}
    headers = {
        "apikey": API_KEY
    }
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={','.join(convert_to)}&base={base}"
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.text

    return json.loads(result)


def get_graph(exchange_to):
    '''
    Returns a matrix containing conversions between all the symbols.
    '''

    timenow = time.strftime('%d-%b-%Y %H:%M:%S', time.gmtime())

    conversion = {}
    conversions = {'_id': timenow, 'data': conversion}
    # print(exchange_to)

    args = ((symb, exchange_to) for symb in exchange_to)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(parallel.get_conversion, args)
        for result in results:
            conversion[result['base']] = result['data']

    return conversions


def store_conversion(conversion):
    '''
    Store the data fetched from the API to MondoDB.
    '''
    mdb_hist_data.insert_one(conversion)


consider_symb = ['AED', 'AUD', 'ARS', 'BRL', 'CAD', 'CHF', 'CNY', 'CUC', 'CZK', 'EGP', 'EUR', 'HKD', 'INR', 'JPY', 'KPW',
                 'LKR', 'RUB', 'SYP', 'TRY', 'TWD', 'USD', 'VND', 'ZAR', 'ZWL']


send_symbs = consider_symb[:10]
conversion_data = get_graph(send_symbs)
store_conversion(conversion_data)

ArbObj = Arbitrage(conversion_data, mdb_db)
