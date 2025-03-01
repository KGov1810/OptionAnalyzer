from api.cboe.cboe import CboeApi
from api.barchart.barchart import BarchartApi
from api.euronext.euronext import EuronextApi

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
    barchart.get_option()

def run_euronext_extracts():
    """ 
    will test each extract
    """
    # Initialize
    euronext = EuronextApi()
    # Test all functions by default
    euronext.get_option_quotes(ticker="META")
    
if __name__ == '__main__':
    run_cboe_extracts()
