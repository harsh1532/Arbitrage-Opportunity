#!/usr/bin/env python
# coding: utf-8
from API_Key import API_KEY
import requests
import json


def get(val):
    return val


def get_conversion(args):
    base, convert_to = args[0], args[1]
    payload = {}
    headers = {
        "apikey": API_KEY
    }
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={','.join(convert_to)}&base={base}"
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.text
    return {'base': base, 'data': json.loads(result)}
