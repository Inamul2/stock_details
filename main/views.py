import json

from django.http import HttpResponse
from django.shortcuts import render
import requests


def home(request):
    return render(request, "main/form.html")


def home1(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}.BSE&outputsize=full&apikey=T1X18M6KUI99HQJB'

        r = requests.get(url)
        data = r.json()
        k = data['Time Series (Daily)']
        iocl_key = []
        iocl_value = []
        count = 0
        for lm in k:
            if count == 10:
                break
            else:
                count += 1
                iocl_key.append(lm)
                iocl_value.append(k[lm]['2. high'])

        iocl_key = [ele for ele in reversed(iocl_key)]
        iocl_value = [ele for ele in reversed(iocl_value)]
        params = {'last_traded_price': k[list(k.keys())[0]].get('4. close'),
                  'price_change_today': float(k[list(k.keys())[0]]['2. high']) - float(k[list(k.keys())[0]]['3. low']),
                  'percent_price_change_in_last_2_weeks': ((float(k[list(k.keys())[0]]['2. high']) - float(
                      k[list(k.keys())[10]]['2. high'])) / float(k[list(k.keys())[10]]['2. high'])) * 100,
                  'iocl_key': iocl_key, 'iocl_value' : iocl_value
                  }

        return HttpResponse(json.dumps(params))
