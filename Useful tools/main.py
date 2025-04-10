from api.cboe.cboe import CboeApi
from api.barchart.barchart import BarchartApi
from api.euronext.euronext import EuronextApi
from api.nasdaq.nasdaq import NasdaqApi
from api.eurex.eurex import EurexApi
from api.nse.nse import NseApi
from api.cme.cme import CmeApi
from api.leonteq.leonteq import LeonteqApi

def run_cboe_extracts():
    """ 
    will test each extract
    """
    # Initialize
    cboe = CboeApi()
    
    # Test all functions by default
    result1 = cboe.get_option_quotes()
    result2 = cboe.get_cboe_all_tickers()
    result3 = cboe.get_cboe_option_tickers()
    result4 = cboe.get_cboe_future_tickers()
    result5 = cboe.get_future_quotes()
    result6 = cboe.get_intraday_quotes()
    result7 = cboe.get_historical_quotes1()
    result8 = cboe.get_historical_quotes2()
    result9 = cboe.get_cboe_country_mapping()
    result10 = cboe.get_resume1_indices()
    result11 = cboe.get_resume2_indices()
    result12 = cboe.get_implied_correlation_quotes()
    result13 = cboe.get_last_quotes()
    result14 = cboe.get_historical_resume()
    
def run_barchart_extracts():
    """ 
    will test each extract
    """
    # Initialize
    barchart = BarchartApi()
    # Test all functions by default
    barchart.get_option_quotes()

def run_euronext_extracts():
    """ 
    will test each extract
    """
    # Initialize
    euronext = EuronextApi()
    # Test all functions by default
    euronext.get_option_quotes()
    
def run_nasdaq_extracts():
    """ 
    will test each extract
    """
    # Initialize
    nasdaq = NasdaqApi()
    # Test all functions by default
    nasdaq.get_option_quotes()
    
def run_eurex_extracts():
    """ 
    will test each extract
    """
    # Initialize
    eurex = EurexApi()
    # Test all functions by default
    eurex.get_all_tickers()
    
def run_nse_extracts():
    """ 
    will test each extract
    """
    # Initialize
    nse = NseApi()
    # Test all functions by default
    nse.get_option_quotes()
    
def run_cme_extracts():
    """ 
    will test each extract
    """
    # Initialize
    cme = CmeApi()
    # Test all functions by default
    cme.get_option_quotes()

def run_leonteq_extracts():
    """ 
    will test each extract
    """
    # Initialize
    leonteq = LeonteqApi()
    # Test all functions by default
    # result = leonteq.get_product_detail()
    # result = leonteq.get_product_timeseries()
    result = leonteq.search_products()

if __name__ == '__main__':
    run_leonteq_extracts()
