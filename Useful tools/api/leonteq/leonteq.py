import pandas as pd
import requests
import json


class BaseExtractor:
    def __init__(self, base_url=None, headers=None):
        pass
    def _make_request(self, url, params=None):
        pass

class LeonteqApi(BaseExtractor):
    
    def __init__(self):
        super().__init__()
        
    def get_product_detail(self, isin:str="CH1345426105"):
        """ 
        Should define asset_class otehrwise doesn't find the option chain
        https://structuredproducts-ch.leonteq.com/isin/CH1345426105
        """
        URL = f"https://structuredproducts-ch.leonteq.com/api/product-model/details/isin/{isin}"

        HEADERS = {
            'accept':'*/*',
            'accept-encoding':'identity',
            'accept-language':'fr-CH',
            'cache-control':'no-cache',
            'cookie':'language_id=4; JSESSIONID=785D6EDE52D375AF34DF79E50D5B8E0A; dmid=9df4416c-a13a-437c-ad23-b8a5a069ef3b; incap_ses_1517_1286391=usblNe/XD0FUQLtSrncNFQ8bxmcAAAAAClaI6sgw57bPc5Wg/2HO+Q==; sitevisitscookie=1; opvc=5fa3412d-acd0-44f4-b140-90e351d32592; _gcl_au=1.1.588739576.1741037097; _ga=GA1.1.84543111.1741037097; _ga_WD2Z3T3ZVL=GS1.1.1741037097.1.1.1741037151.0.0.0',
            'pragma':'no-cache',
            'priority':'u=1, i',
            'referer':'https://structuredproducts-ch.leonteq.com/isin/CH1345426105',
            'sec-ch-ua':'"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }

        PARAMS = {
            "language_id": 4
        }

        s = requests.Session()
        r = s.get(URL, headers=HEADERS, params=PARAMS)
        data = json.loads(r.text)
        data = data['product']
        
        clean_data = {}
    
        # Process each key in the data
        for key, info in data.items():
            # Handle different types of values
            if "value" in info:
                clean_data[key] = info["value"]
            elif "raw" in info:
                clean_data[key] = info["raw"]
            elif isinstance(info, dict) and len(info) > 0:
                # Handle nested dictionaries like coupons, ask, bid
                for subkey, subvalue in info.items():
                    clean_data[f"{key}_{subkey}"] = subvalue
        
        # Create a DataFrame with a better visual format
        df = pd.DataFrame([clean_data]).T.reset_index()
        df.columns = ["Parameter", "Value"]
        
        return df
    
    def get_product_timeseries(self, isin:str="CH1345426105"):
        """ 
        Should define asset_class otehrwise doesn't find the option chain
        https://structuredproducts-ch.leonteq.com/isin/CH1345426105
        """
        URL = f"https://structuredproducts-ch.leonteq.com/website-api/feed/timeseries/request"

        HEADERS = {
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control':'no-cache',
            'cookie':'language_id=4; JSESSIONID=785D6EDE52D375AF34DF79E50D5B8E0A; dmid=9df4416c-a13a-437c-ad23-b8a5a069ef3b; incap_ses_1517_1286391=usblNe/XD0FUQLtSrncNFQ8bxmcAAAAAClaI6sgw57bPc5Wg/2HO+Q==; sitevisitscookie=1; opvc=5fa3412d-acd0-44f4-b140-90e351d32592; _gcl_au=1.1.588739576.1741037097; _ga=GA1.1.84543111.1741037097; _ga_WD2Z3T3ZVL=GS1.1.1741037097.1.1.1741037152.0.0.0',
            'pragma':'no-cache',
            'priority':'u=1, i',
            'content-length':'33',
            'content-type':'application/json',
            'referer':'https://structuredproducts-ch.leonteq.com/isin/CH1345426105',
            'origin':'https://structuredproducts-ch.leonteq.com',
            'authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJMZW9udGVxIFdlYnNpdGUgQ0giLCJhenAiOiJzcC5sZW9udGVxLmNvbSIsInJvbGVzIjpbXSwiaXNzIjoiaHR0cHM6Ly9zdHJ1Y3R1cmVkcHJvZHVjdHMubGVvbnRlcS5jb20vd2Vic2l0ZS1hcGkvYXV0aC9yZWFsbXMvd2Vic2l0ZS1hcGkiLCJuYW1lIjoiTEVPTlRFUSIsImV4cCI6MTk1NjczNzE4NCwiaWF0IjoxNjQxMzc3MTg0fQ.pL3NHCftsdZgeyJaYE9FzY2PhhKpQPlwzo8i9Zd-7gchs8QAc3CdyA4e4SoFFcVelLVmny7UwoV8lfg3rWGmfNxmVrUzVgWvgncRS1L5OJlrb5lQ-XrWIxFUN2ifeDH78h4TRk44HIF5NLYr-985PfaUrcLrC-R67dWgYuwczmmkBFG0oWKk4ynXQRP9fFkd1aMWwGdAwv_toM3semchkDlakk6l8mboSQ6ALlfR0qLPqTMLhmjZaMdAkZdR2hWidWG6ILOpFlWt6B2I2Pdbwdo4K2jQAtML0k4KA1FX6zznhTLigyXWBoAzXOxIm1htEt-oiieCRs-LADhfB7e7dw',
            'sec-ch-ua':'"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }

        PARAMS = {
            # 'from':'202502280100',
            # 'to':'202503032335'
        }
        
        PAYLOAD = {"sophisInternalIds": ["201168"]}

        s = requests.Session()
        r = s.post(URL, headers=HEADERS, params=PARAMS, json=PAYLOAD)
        data = json.loads(r.text)
        data 
        
        return data
    
    def search_products(self, isin:str="CH1345426105"):
        """ 
        Should define asset_class otehrwise doesn't find the option chain
        https://structuredproducts-ch.leonteq.com/isin/CH1345426105
        """
        url = "https://structuredproducts-ch.leonteq.com/api/product-model/search"

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": "https://structuredproducts-ch.leonteq.com",
            "Referer": "https://structuredproducts-ch.leonteq.com/search/all-products",
            'cookie':'language_id=4; JSESSIONID=785D6EDE52D375AF34DF79E50D5B8E0A; dmid=9df4416c-a13a-437c-ad23-b8a5a069ef3b; incap_ses_1517_1286391=usblNe/XD0FUQLtSrncNFQ8bxmcAAAAAClaI6sgw57bPc5Wg/2HO+Q==; sitevisitscookie=1; opvc=5fa3412d-acd0-44f4-b140-90e351d32592; _gcl_au=1.1.588739576.1741037097; _ga=GA1.1.84543111.1741037097; _ga_WD2Z3T3ZVL=GS1.1.1741037097.1.1.1741037152.0.0.0',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        params = {
            "resultsPerPage": "50",
            "partner": "LEONTEQ",
            # "regions": ["CH"],
            # "language": "fr",
            # "currencies": [],
            # "issuers": [],
            # "assetClasses": [],
            # "barrierLevelRanges": [],
            # "barrierTypes": [],
            # "displayColumns": [],
            # "distanceToBarriers": [],
            # "marketVenues": [],
            # "maturityRangeKey": "",
            # "omni": "",
            # "pageNumber": "1",
            # "productCategories": [],
            # "productGroups": [],
            # "productTypes": [],
            # "strikeLevelRanges": [],
            # "underlyingSearchString": "",
            # "underlyings": []
        }

        response = requests.post(url, json=params, headers=headers)
        data = response.text
        
        return data


        