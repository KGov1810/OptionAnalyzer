import requests
from urllib.parse import unquote
import pandas as pd
from datetime import datetime


def get_url():

    geturl=r'https://www.barchart.com/stocks/quotes/AAPL/options'
    

    getheaders={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }

    getpay={
        'page': 'all'
        }

    s=requests.Session()
    r=s.get(geturl,params=getpay, headers=getheaders)

    return r,s


# ----------------------------------------------------------------------------------------------------------

def get_api_options(r,s, ticker):

    apiurl=r'https://www.barchart.com/proxies/core-api/v1/options/get'

    headers={
        'accept': 'application/json',
        'accept-encoding': 'gzip',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'x-xsrf-token': unquote(unquote(s.cookies.get_dict()['XSRF-TOKEN']))
    }

    payload={
            'fields': 'symbol,baseSymbol,strikePrice,lastPrice,theoretical,volatility,delta,gamma,theta,vega,rho,volume,openInterest,volumeOpenInterestRatio,optionType,daysToExpiration,expirationDate,tradeTime,averageVolatility,historicVolatility30d,baseNextEarningsDate',
            "baseSymbol": str(ticker),
            "groupBy":"optionType",
            "expirationDate":"",
            "meta":"field.shortName,expirations",
            "orderBy":"strikePrice",
            "orderDir":"asc",
            "limit" : 10000
        }

    r=s.get(apiurl,params=payload, headers=headers)
    j=r.json()

    return j


r,s = get_url()
tickers = ['AAPL']
data = {}
data = {ticker : get_api_options(r,s,ticker) for ticker in tickers}
data