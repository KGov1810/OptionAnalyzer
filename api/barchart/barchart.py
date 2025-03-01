import pandas as pd
import requests
from urllib.parse import unquote
from datetime import datetime
from api.barchart.config import DEFAULT_HEADERS

class BaseExtractor:
    """
    Base class for API data extractors.
    
    This class provides common functionality for making API requests,
    handling authentication, and processing responses.
    """
    
    def __init__(self, base_url=None, headers=None):
        """
        Initialize the base extractor with common properties.
        
        Args:
            base_url (str, optional): Base URL for API endpoints
            headers (dict, optional): Default headers for API requests
        
        Note:
            If headers are not provided, DEFAULT_HEADERS from config will be used
        """
        self.base_url = base_url
        self.headers = DEFAULT_HEADERS
        self.session = requests.Session()
    
    def _make_request(self, url, params=None):
        """
        Make an HTTP request and return the JSON response.
        
        This method handles authentication token management and performs
        the actual HTTP request to the API endpoint.
        
        Args:
            url (str): Endpoint URL
            params (dict, optional): Query parameters
            
        Returns:
            dict: JSON response from the API
            
        Raises:
            Exception: If request fails with non-200 status code
            ValueError: If JSON parsing fails
            ConnectionError: If network connection fails
        """
        token, session = self._get_token_and_session()
        self.headers["x-xsrf-token"] = token
        
        response = session.get(url=url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
            
        return response.json()
    
    def _get_token_and_session(self):
        """
        Obtain authentication token and session for Barchart API.
        
        This method creates a session and retrieves the XSRF token required
        for authenticated API requests to Barchart.
        
        Returns:
            tuple: (token, request_session) containing authentication token and active request session
            
        Raises:
            ConnectionError: If unable to connect to the authentication endpoint
            ValueError: If token extraction fails
        """
        URL = 'https://www.barchart.com/stocks/quotes/AAPL/options'

        PARAMS = {'page': 'all'}

        session = requests.Session()
        r = session.get(URL, params=PARAMS, headers=self.headers)
        token = unquote(unquote(session.cookies.get_dict()['XSRF-TOKEN']))
        return (token, session)
    
class BarchartApi(BaseExtractor):
    """
    Client for the Barchart API providing access to options data.
    
    This class implements specific endpoints for retrieving financial data
    from Barchart, including options quotes and related information.
    """
    
    def __init__(self):
        """
        Initialize the Barchart API client.
        
        Sets up the client with default configuration and inherits
        base functionality from BaseExtractor.
        """
        super().__init__()
        
    def get_option_quotes(self, ticker="AAPL"):
        """
        Retrieve options quotes data for a specific ticker symbol.
        
        Fetches comprehensive options data including strike prices, Greeks,
        volatility metrics, and other relevant trading information.
        
        Args:
            ticker (str): Stock ticker symbol (default: "AAPL")
            
        Returns:
            pandas.DataFrame: DataFrame containing options data with the following columns:
                - symbol: Option contract symbol
                - baseSymbol: Underlying stock symbol
                - strikePrice: Strike price of the option
                - lastPrice: Last traded price
                - theoretical: Theoretical option price
                - volatility: Implied volatility
                - delta, gamma, theta, vega, rho: Option Greeks
                - volume: Trading volume
                - openInterest: Open interest
                - volumeOpenInterestRatio: Volume to open interest ratio
                - optionType: PUT or CALL
                - daysToExpiration: Days until option expiration
                - expirationDate: Option expiration date
                - tradeTime: Time of last trade
                - averageVolatility: Average implied volatility
                - historicVolatility30d: 30-day historical volatility
                - baseNextEarningsDate: Next earnings date for underlying
            
        Raises:
            Exception: If API request fails
            KeyError: If response format is unexpected
            ValueError: If data parsing fails
            
        Example:
            >>> api = BarchartApi()
            >>> options_data = api.get_option_quotes("MSFT")
            >>> call_options = options_data[options_data['optionType'] == 'CALL']
        """
        url = 'https://www.barchart.com/proxies/core-api/v1/options/get'
        
        params = {
            'fields': 'symbol,baseSymbol,strikePrice,lastPrice,theoretical,volatility,delta,gamma,theta,vega,rho,volume,openInterest,volumeOpenInterestRatio,optionType,daysToExpiration,expirationDate,tradeTime,averageVolatility,historicVolatility30d,baseNextEarningsDate',
            "baseSymbol": ticker,
            "groupBy": "optionType",
            "expirationDate": "",
            "meta": "field.shortName,expirations",
            "orderBy": "strikePrice",
            "orderDir": "asc",
            "limit": 10000
        }
        
        response = self._make_request(url, params)
        df = pd.DataFrame(response['data'])
        return df