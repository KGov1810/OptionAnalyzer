import pandas as pd
import requests
from datetime import datetime
from api.nasdaq.config import DEFAULT_HEADERS

class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass

class NasdaqApi(BaseExtractor):
    
    def __init__(self):
        super().__init__()
        
    def get_option_quotes(self,ticker:str="TSLA",asset_class:str="stocks"):
        """ 
        Should define asset_class otehrwise doesn't find the option chain
        https://www.nasdaq.com/market-activity/stocks/tsla/option-chain
        #TODO: Need to format and organize the output
        """
        
        apiurl=f'https://api.nasdaq.com/api/quote/{ticker}/option-chain'

        headers={
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.nasdaq.com',
            'referer': 'https://www.nasdaq.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        payload={
                'assetclass': asset_class,
                'limit':100000,
                'fromdate': 'all',
                'todate': 'undefined',
                'excode': 'oprac',
                'callput': 'callput',
                'money' : 'all',
                'type': 'all'
            }

        s=requests.Session()
        r=s.get(apiurl, headers=headers, params = payload)
        j=r.json()
        df = pd.DataFrame(j['data']['table']['rows'])
        return df
        