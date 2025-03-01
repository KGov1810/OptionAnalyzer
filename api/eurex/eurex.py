import pandas as pd
import requests
from datetime import datetime
from api.euronext.config import DEFAULT_HEADERS

class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass
    
class EurexApi(BaseExtractor):
    
    def __init__(self):
        super().__init__()
        
        
    def get_all_tickers(self,ticker:str="AAI"):
        
        url =r"https://www.eurex.com/ex-en!dynSearch/"

        s=requests.Session()
        r=s.get(url)
        j=r.json()
        df = pd.DataFrame(j['items'])
        return df
        