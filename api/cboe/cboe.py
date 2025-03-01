import pandas as pd
import requests
from datetime import datetime
from api.cboe.config import DEFAULT_HEADERS

class BaseExtractor:
    """Base class for API data extractors."""
    
    def __init__(self, base_url=None, headers=None):
        """
        Initialize the base extractor with common properties.
        
        Args:
            base_url (str, optional): Base URL for API endpoints
            headers (dict, optional): Default headers for API requests
        """
        self.base_url = base_url
        self.headers = DEFAULT_HEADERS
        self.session = requests.Session()
    
    def _make_request(self, url, params=None):
        """
        Make an HTTP request and return the JSON response.
        
        Args:
            url (str): Endpoint URL
            params (dict, optional): Query parameters
            headers (dict, optional): Custom headers to override defaults
            
        Returns:
            dict: JSON response
            
        Raises:
            Exception: If request fails
        """
        response = self.session.get(url=url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
            
        return response.json()


class CboeApi(BaseExtractor):
    """
    Client for the CBOE API providing access to options, futures, and market data.
    """
    
    def __init__(self):
        """
        Initialize the CBOE API client.
        
        Args:
            api_key (str, optional): API key for authentication (if required)
        """
        base_url = "https://cdn.cboe.com/api/global"
        super().__init__(base_url=base_url)
    
    def get_option_quotes(self, ticker="AAPL"):
        """
        Retrieve option quotes for a specific ticker.
        
        Args:
            ticker (str): Stock ticker symbol (default: "AAPL")
            
        Returns:
            pandas.DataFrame: Options data with parsed fields
            
        Raises:
            Warning: If no data is returned for the ticker
        """
        url = f"{self.base_url}/delayed_quotes/options/{ticker}.json"
        response = self._make_request(url)
        df = pd.DataFrame(response["data"]["options"])
        
        if df.empty:
            raise Warning(f"{ticker} Empty")
        
        # Extract timestamp
        extract_time = datetime.now()
        
        # Process option data
        df["ticker"] = ticker
        df["time"] = extract_time.strftime(format="%Y-%m-%d %H:%M:%S")
        df.rename(columns={"iv": "implied_vol", "option": "option_name", "theo": "theo_price"}, inplace=True)
        
        # Clean up ticker name for parsing
        ticker_clean = ticker.replace("_", "")
        df["option_name_clean"] = df["option_name"].str.replace(ticker_clean, "", regex=False)
        
        # Parse option details
        df["maturity"] = df["option_name_clean"].apply(self._get_option_maturity)
        df["strike"] = df["option_name_clean"].apply(self._get_option_strike)
        df["option_type"] = df["option_name_clean"].apply(self._get_option_type)
        
        return df
    
    def _get_option_maturity(self, option_name):
        """
        Extract maturity date from option_name in format YYMMDD and convert to YYYY-MM-DD.
        
        Args:
            option_name (str): Option identifier
            
        Returns:
            str: Formatted maturity date
        """
        maturity_code = option_name[:6]
        year = '20' + maturity_code[:2]  # Convert '24' to '2024'
        month = maturity_code[2:4]       # Extract month
        day = maturity_code[4:6]         # Extract day
        return f"{year}-{month}-{day}"   # Return in 'YYYY-MM-DD' format

    def _get_option_strike(self, option_name):
        """
        Extract strike price from option_name.
        
        Args:
            option_name (str): Option identifier
            
        Returns:
            float: Strike price
        """
        strike = float(option_name[7:]) / 1000
        return strike

    def _get_option_type(self, option_name):
        """
        Extract option type from option_name.
        
        Args:
            option_name (str): Option identifier
            
        Returns:
            str: "CALL", "PUT", or None
        """
        if option_name[6] == "C":
            return "CALL"
        elif option_name[6] == "P":
            return "PUT"
        else:
            return None
    
    def get_cboe_all_tickers(self):
        """
        Retrieve all available ticker symbols from CBOE.
        
        Returns:
            pandas.DataFrame: DataFrame containing all tickers
        """
        url = f"{self.base_url.split('/api')[0]}/api/global/delayed_quotes/symbol_book/symbol-book.json"
        response = self._make_request(url)
        df = pd.DataFrame(response['data'])
        return df
    
    def get_cboe_option_tickers(self):
        """
        Retrieve available option ticker symbols from CBOE.
        
        Returns:
            pandas.DataFrame: DataFrame containing option tickers
        """
        url = f"{self.base_url}/delayed_quotes/symbol_book/option-roots.json"
        response = self._make_request(url)
        df = pd.DataFrame(response['data'])
        df = pd.DataFrame(df['symbol'].unique())
        df = df.rename(columns={0: 'symbols'})
        df['symbols'] = df['symbols'].str.replace("^", "_", regex=False)
        return df
    
    def get_cboe_future_tickers(self):
        """
        Retrieve available futures ticker symbols from CBOE.
        
        Returns:
            pandas.DataFrame: DataFrame containing futures tickers
        """
        url = f"{self.base_url}/delayed_quotes/symbol_book/futures-roots.json"
        response = self._make_request(url)
        df = pd.DataFrame(response['data'])
        return df
    
    def get_future_quotes(self, ticker="VX"):
        """
        Retrieve futures quotes for a specific ticker.
        
        Args:
            ticker (str): Futures ticker symbol (default: "VX")
            
        Returns:
            pandas.DataFrame: Futures quotes data
        """
        url = 'https://www.cboe.com/us/futures/api/get_quotes_combined/'
        params = {'symbol': ticker,'rootsymbol': 'null'}
        response = self._make_request(url, params=params)
        df = pd.DataFrame(response['data'])
        return df
    
    def get_intraday_quotes(self, ticker="AAPL"):
        """
        Retrieve intraday price quotes for a specific ticker.
        
        Args:
            ticker (str): Stock ticker symbol (default: "AAPL")
            
        Returns:
            pandas.DataFrame: Intraday quotes with timestamp and price data
        """
        url = f"{self.base_url}/delayed_quotes/charts/intraday/{ticker}.json"
        response = self._make_request(url)
    
        df = pd.DataFrame([
            {
                'date': pd.to_datetime(item['datetime']).strftime('%Y-%m-%d'),
                'datetime': pd.to_datetime(item['datetime']),
                'ticker': ticker,
                **item['price'],
                **item['volume']
            } for item in response['data']
        ])
        
        return df
    
    def get_historical_quotes1(self, ticker="VIX", frequency="1Y", asset_type="indices"):
        """
        Retrieve historical quotes using the first method.
        
        Args:
            ticker (str): Ticker symbol (default: "VIX")
            frequency (str): Time period - "1M", "3M", "6M", "1Y" (default: "1Y")
            asset_type (str): Asset category (default: "indices")
            
        Returns:
            pandas.DataFrame: Historical quotes with OHLC data
        """
        url = f"https://www.cboe.com/{asset_type}/data/"
        
        params = {
            "symbol": ticker,
            "timeline": frequency
        }
        
        response = self._make_request(url, params=params)
        df = pd.DataFrame(response["data"], columns=["time", "open", "high", "low", "close"])
        df['time'] = pd.to_datetime(df['time']).dt.strftime("%Y-%m-%d %H:%M:%S")
        return df
    
    def get_historical_quotes2(self, ticker="AAPL"):
        """
        Retrieve historical quotes using the second method.
        
        Args:
            ticker (str): Ticker symbol (default: "VIX")
            
        Returns:
            pandas.DataFrame: Historical quotes data
        """
        url = f"{self.base_url}/delayed_quotes/charts/historical/{ticker}.json"
        response = self._make_request(url)
        df = pd.DataFrame(response["data"])
        return df
    
    def get_cboe_country_mapping(self):
        """
        Retrieve country mapping information from CBOE.
        
        Returns:
            pandas.DataFrame: Country mapping data
        """
        url = f"{self.base_url.split('/api')[0]}/resources/general/countries.json"
        response = self._make_request(url)
        df = pd.DataFrame(response)
        return df
    
    def get_detail_indices(self, indices='european_indices'):
        """
        Retrieve detailed information about market indices.
        
        Args:
            indices (str): Index category - "european_indices", "all_us_indices" (default: "european_indices")
            
        Returns:
            pandas.DataFrame: Detailed index information including constituents
        """
        url = f"{self.base_url}/{indices}/definitions/all-definitions.json"
        response = self._make_request(url)
        
        result = []
        for data in response["data"]:
            result.append({
                "symbol": data["index"].get("symbol", None),
                "isin": data["index"].get("isin", None),
                "short_name": data["index"].get("short_name", None),
                "long_name": data["index"].get("long_name", None),
                "currency": data["index"].get("currency", None),
                "region": data["index"].get("region", None),
                "constituent_symbol": ','.join([item['constituent_symbol'] for item in data["constituents"]])
            })
        
        df = pd.DataFrame(result)
        return df
    
    def get_resume1_indices(self, indices='all_us_indices'):
        """
        Retrieve summary information about indices using the first method.
        
        Args:
            indices (str): Index category - "european_indices", "all_us_indices", "all-indices" (default: "all_us_indices")
            
        Returns:
            pandas.DataFrame: Summary index information
        """
        url = f"{self.base_url}/delayed_quotes/quotes/{indices}.json"
        response = self._make_request(url)
        df = pd.DataFrame(response["data"])
        return df
    
    def get_resume2_indices(self, indices='european_indices'):
        """
        Retrieve summary information about indices using the second method.
        
        Args:
            indices (str): Index category - "european_indices", "all_us_indices", "all-indices" (default: "european_indices")
            
        Returns:
            pandas.DataFrame: Summary index information
        """
        url = f"{self.base_url}/{indices}/index_quotes/all-indices.json"
        response = self._make_request(url)
        df = pd.DataFrame(response["data"])
        return df
    
    def get_implied_correlation_quotes(self, ticker='COR_2024-07-19', year='2024'):
        """
        Retrieve implied correlation quotes.
        
        Args:
            ticker (str): Correlation index ticker (default: "COR_2024-07-19")
            year (str): Year for data (default: "2024")
            
        Returns:
            pandas.DataFrame: Implied correlation data
        """
        url = f"{self.base_url}/delayed_quotes/implied_correlation/{year}/{ticker}.json"
        response = self._make_request(url)
        df = pd.DataFrame(response["data"]["prices"])
        return df
    
    def get_last_quotes(self, ticker="_VIX"):
        """
        Retrieve the latest quotes for a ticker.
        
        Args:
            ticker (str): Ticker symbol (default: "_VIX")
            
        Returns:
            pandas.DataFrame: Latest quote data
        """
        url = f"{self.base_url}/delayed_quotes/quotes/{ticker}.json"
        response = self._make_request(url)
        df = pd.DataFrame(response)
        return df["data"]
    
    def get_historical_resume(self, ticker="_VIX"):
        """
        Retrieve historical summary data for a ticker.
        
        Args:
            ticker (str): Ticker symbol (default: "_VIX")
            
        Returns:
            pandas.DataFrame: Historical summary data
        """
        url = f"{self.base_url}/delayed_quotes/historical_data/{ticker}.json"
        response = self._make_request(url)
        df = pd.DataFrame(response)
        return df["data"]