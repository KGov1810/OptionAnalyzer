import pandas as pd
import requests
from datetime import datetime
from api.euronext.config import DEFAULT_HEADERS

class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass

class EuronextApi(BaseExtractor):
    
    def __init__(self):
        super().__init__()
        
    def get_option_quotes(self,ticker:str="AAI"):
        
        apiurl=f'https://live.euronext.com/en/ajax/getPricesOptionsAjax/stock-options/{ticker}/DAMS'

        headers={
            'accept': '*/*',
            'accept-encoding': 'gzip',
            'accept-language': 'en-US,en;q=0.9',
            'origin' : 'https://live.euronext.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            # 'content-length': 1000
        }

        s=requests.Session()
        r=s.get(apiurl, headers=headers)
        j=r.json()
        df = pd.DataFrame(j['extended'][0]['rowc'])
        return df
        